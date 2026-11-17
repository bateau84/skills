# Viper WatchConfig and Hot Reload

## Basic setup

```go
viper.OnConfigChange(func(e fsnotify.Event) {
    log.Printf("config changed: %s (op: %s)", e.Name, e.Op)
    // re-read affected values and apply them
})
viper.WatchConfig()
```

`WatchConfig` starts a background goroutine that watches the config file using fsnotify. Call it after `ReadInConfig`.

## The atomic-rename trap

Editors often replace files via atomic rename. Viper watches the parent directory and filters events for the configured filename; a rename into the watched path can therefore produce a reload. Event ordering, duplicate notifications and transient malformed writes still need testing on the deployed filesystem. Do not assume Viper watches only the original file inode.

**Test the real write patterns:** cover a direct write and a temp-file-plus-rename replacement, including a rejected malformed candidate. Event counts are not stable across platforms; assert the resulting validated configuration, not exactly one fsnotify event. Register the callback before starting the watcher, and retain an owned immutable/synchronized application snapshot.

## Race-safe reload pattern

Config reload happens in a background goroutine. Any shared state updated in `OnConfigChange` must be synchronized:

```go
type Config struct {
    mu       sync.RWMutex
    LogLevel string `mapstructure:"log_level"`
    MaxConn  int    `mapstructure:"max_conn"`
}

var cfg Config

viper.OnConfigChange(func(e fsnotify.Event) {
    var newCfg Config
    if err := viper.Unmarshal(&newCfg); err != nil {
        log.Printf("error reloading config: %v", err)
        return  // keep old config on error
    }

    cfg.mu.Lock()
    cfg.LogLevel = newCfg.LogLevel
    cfg.MaxConn = newCfg.MaxConn
    cfg.mu.Unlock()

    log.Printf("config reloaded: log_level=%s", newCfg.LogLevel)
})
```

Reads use `cfg.mu.RLock()` around the snapshot fields. Do not concurrently read or mutate the Viper instance itself during reload: Viper is not a synchronization primitive. Decode and validate in the watcher path, then publish the application snapshot under its lock.

## Debouncing rapid changes

Some filesystems fire multiple events per save. Debounce to avoid reloading multiple times:

```go
var reloadTimer *time.Timer
var reloadMu sync.Mutex

viper.OnConfigChange(func(e fsnotify.Event) {
    reloadMu.Lock()
    defer reloadMu.Unlock()
    if reloadTimer != nil {
        reloadTimer.Stop()
    }
    reloadTimer = time.AfterFunc(100*time.Millisecond, func() {
        applyNewConfig()
    })
})
```

## Validating config before applying

Always validate reloaded config before applying it — an invalid config mid-reload should keep the previous working config:

```go
viper.OnConfigChange(func(e fsnotify.Event) {
    var candidate Config
    if err := viper.Unmarshal(&candidate); err != nil {
        log.Printf("reload: invalid config, keeping previous: %v", err)
        return
    }
    if err := validate(candidate); err != nil {
        log.Printf("reload: validation failed, keeping previous: %v", err)
        return
    }
    applyConfig(candidate)
})
```

## Stopping the watcher

There is no documented way to stop `WatchConfig` once started. Design your application so that the watcher's lifetime matches the process lifetime. For testing, create a new `viper.New()` instance per test — the watcher goroutine may retain the Viper instance, so do **not** assume instance garbage collection stops it. Treat process-lifetime watches as deliberate and avoid starting uncontrolled watches in short-lived tests.
