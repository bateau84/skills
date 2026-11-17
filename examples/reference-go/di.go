package reference

import "github.com/samber/do/v2"

type Config struct{ Name string }
type Service struct{ Name string }

func NewServices() *do.RootScope {
	i := do.New()
	do.ProvideValue(i, Config{Name: "production"})
	do.Provide(i, func(i do.Injector) (*Service, error) {
		cfg, err := do.Invoke[Config](i)
		if err != nil {
			return nil, err
		}
		return &Service{Name: cfg.Name}, nil
	})
	return i
}
