# Viper Unmarshal and Struct Mapping

## Basic Unmarshal

```go
type Config struct {
    Port     int    `mapstructure:"port"`
    Host     string `mapstructure:"host"`
    LogLevel string `mapstructure:"log_level"`
    Database struct {
        DSN     string `mapstructure:"dsn"`
        MaxConn int    `mapstructure:"max_conn"`
    } `mapstructure:"database"`
}

var cfg Config
if err := viper.Unmarshal(&cfg); err != nil {
    return fmt.Errorf("decoding config: %w", err)
}
```

## mapstructure tags

Always use `mapstructure` tags. Without them, mapstructure falls back to case-insensitive field name matching, which works for simple cases but silently fails for:

- Nested structs where the outer key uses an underscore (`max_conn` → `MaxConn`)
- Unexported fields
- Fields where the Go name does not match the config key

```go
// ✓ Good — explicit and immune to rename surprises
type TLSConfig struct {
    CertFile string `mapstructure:"cert_file"`
    KeyFile  string `mapstructure:"key_file"`
    Enabled  bool   `mapstructure:"enabled"`
}

// ✗ Fragile — relies on case-folding; breaks when config key uses underscores
type TLSConfig struct {
    CertFile string  // viper key "certfile" or "CertFile", not "cert_file"
    KeyFile  string
    Enabled  bool
}
```

## UnmarshalKey — extracting a sub-tree

```go
type DatabaseConfig struct {
    DSN     string `mapstructure:"dsn"`
    MaxConn int    `mapstructure:"max_conn"`
}

var dbCfg DatabaseConfig
if err := viper.UnmarshalKey("database", &dbCfg); err != nil {
    return fmt.Errorf("decoding database config: %w", err)
}
```

Prefer `UnmarshalKey` over `viper.Sub` + `Unmarshal` — fewer nil checks and less boilerplate.

## time.Duration

Viper's `GetDuration` and default `Unmarshal` decoder already handle duration strings (`"1h30m"`, `"500ms"`) in supported versions; Viper v1.20+ uses `github.com/go-viper/mapstructure/v2`. **Do not add duration or weak-decoding hooks just to restore default behavior.** Add a decode hook only for a custom target type or a deliberate override, and compose it with the existing `dc.DecodeHook`.

```go
import "github.com/go-viper/mapstructure/v2"

var cfg Config
err := viper.Unmarshal(&cfg, func(dc *mapstructure.DecoderConfig) {
    dc.DecodeHook = mapstructure.ComposeDecodeHookFunc(
        mapstructure.StringToTimeDurationHookFunc(),
        mapstructure.StringToSliceHookFunc(","),
        dc.DecodeHook,
    )
})
```

`StringToTimeDurationHookFunc` handles `"1h30m"` → `time.Duration`. `StringToSliceHookFunc(",")` handles `"a,b,c"` → `[]string{"a", "b", "c"}`.

## net.IP and custom types

```go
import "github.com/go-viper/mapstructure/v2"

func stringToIPHookFunc() mapstructure.DecodeHookFunc {
    return func(f reflect.Type, t reflect.Type, data interface{}) (interface{}, error) {
        if f.Kind() != reflect.String || t != reflect.TypeOf(net.IP{}) {
            return data, nil
        }
        ip := net.ParseIP(data.(string))
        if ip == nil {
            return nil, fmt.Errorf("invalid IP address: %s", data)
        }
        return ip, nil
    }
}
```

## Squash for embedded structs

```go
type BaseConfig struct {
    LogLevel string `mapstructure:"log_level"`
    Debug    bool   `mapstructure:"debug"`
}

type ServerConfig struct {
    BaseConfig `mapstructure:",squash"`  // merge BaseConfig fields at this level
    Port       int    `mapstructure:"port"`
}
```

Without `,squash`, the base config must be nested under a `baseconfig` key in the config file.

## Remain for unknown keys

```go
type Config struct {
    Port     int                    `mapstructure:"port"`
    Remain   map[string]interface{} `mapstructure:",remain"`
}
```

Extra keys from the config file are collected in `Remain` instead of being silently dropped. Useful for forward compatibility.

## Weak decoding

Viper's default Unmarshal decoder already enables weak type decoding (for example string `"true"` → bool `true`). The following makes that policy explicit; it is **not needed** to restore the default. Validate security-sensitive fields more strictly when coercion could hide mistakes:

```go
var cfg Config
err := viper.Unmarshal(&cfg, func(dc *mapstructure.DecoderConfig) {
    dc.WeaklyTypedInput = true
})
```

Use with caution — weak decoding can hide bugs where a wrong value type is silently converted.
