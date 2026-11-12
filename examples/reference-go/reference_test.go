package reference

import (
	"errors"
	"github.com/samber/do/v2"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestViperMissingConfigAndDefaultDuration(t *testing.T) {
	v := viper.New()
	v.SetConfigName("absent")
	v.AddConfigPath(t.TempDir())
	err := v.ReadInConfig()
	var value viper.ConfigFileNotFoundError
	if !errors.As(err, &value) {
		t.Fatalf("expected value missing-config error: %v", err)
	}
	v.Set("timeout", "2s")
	var cfg struct {
		Timeout time.Duration `mapstructure:"timeout"`
	}
	if err := v.Unmarshal(&cfg); err != nil || cfg.Timeout != 2*time.Second {
		t.Fatalf("default duration hook: %+v %v", cfg, err)
	}
}
func TestViperEnvOnlyUnmarshal(t *testing.T) {
	t.Setenv("TEST_HOST", "localhost")
	v := viper.New()
	v.SetEnvPrefix("TEST")
	v.AutomaticEnv()
	var cfg struct {
		Host string `mapstructure:"host"`
	}
	if err := v.BindEnv("host"); err != nil {
		t.Fatal(err)
	}
	if err := v.Unmarshal(&cfg); err != nil || cfg.Host != "localhost" {
		t.Fatalf("env binding: %+v %v", cfg, err)
	}
}
func TestDICloneOverrideAndMissingProvider(t *testing.T) {
	original := NewServices()
	clone := original.Clone()
	do.OverrideValue(clone, Config{Name: "test"})
	if got := do.MustInvoke[*Service](clone).Name; got != "test" {
		t.Fatal(got)
	}
	if got := do.MustInvoke[*Service](original).Name; got != "production" {
		t.Fatal(got)
	}
	if _, err := do.Invoke[*Service](do.New()); err == nil {
		t.Fatal("missing provider must be a runtime error")
	}
}
func TestTestifyDeepEqualityIsNotIdentity(t *testing.T) {
	a, b := &Config{Name: "same"}, &Config{Name: "same"}
	assert.Equal(t, a, b)
	assert.NotSame(t, a, b)
}
