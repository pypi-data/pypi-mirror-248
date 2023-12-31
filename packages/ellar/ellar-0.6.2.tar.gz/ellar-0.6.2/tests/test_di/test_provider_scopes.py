import pytest
from ellar.di import EllarInjector, ProviderConfig, has_binding
from ellar.di.exceptions import DIImproperConfiguration
from ellar.di.scopes import RequestScope, SingletonScope, TransientScope
from injector import UnsatisfiedRequirement, inject

from .examples import AnyContext, Foo, IContext, TransientRequestContext


@pytest.mark.parametrize(
    "action, base_type, concrete_type, ref_type, expected_scope",
    [
        ("register_instance", Foo(), None, Foo, SingletonScope),
        ("register_instance", Foo(), Foo, Foo, SingletonScope),
        ("register_singleton", Foo, None, Foo, SingletonScope),
        ("register_singleton", Foo, Foo, Foo, SingletonScope),
        ("register_transient", Foo, None, Foo, TransientScope),
        ("register_transient", Foo, Foo, Foo, TransientScope),
        ("register_scoped", Foo, None, Foo, RequestScope),
        ("register_scoped", Foo, Foo, Foo, RequestScope),
        ("register_exact_singleton", Foo, None, Foo, SingletonScope),
        ("register_exact_transient", Foo, None, Foo, TransientScope),
        ("register_exact_scoped", Foo, None, Foo, RequestScope),
    ],
)
def test_container_scopes(action, base_type, concrete_type, ref_type, expected_scope):
    container = EllarInjector().container
    container_action = getattr(container, action)
    if concrete_type:
        container_action(base_type, concrete_type)
    else:
        container_action(base_type)
    binding = container.get_binding(ref_type)
    assert binding[0].scope is expected_scope


@pytest.mark.asyncio
async def test_request_transient_scope_instance():
    injector = EllarInjector(auto_bind=False)
    ProviderConfig(IContext, use_class=TransientRequestContext).register(
        injector.container
    )

    # resolving RequestScope Providers outside RequestServiceProvider will behave like TransientScope
    assert injector.get(IContext) != injector.get(IContext)
    assert isinstance(injector.get(IContext), TransientRequestContext)

    async with injector.create_asgi_args() as request_provider:
        # resolving RequestScope during request will behave like singleton
        assert request_provider.get(IContext) == request_provider.get(IContext)


@pytest.mark.asyncio
async def test_request_scope_instance():
    injector = EllarInjector(auto_bind=False)
    ProviderConfig(IContext, use_class=AnyContext).register(injector.container)

    # resolving RequestScope Providers outside RequestServiceProvider will behave like TransientScope

    with pytest.raises(UnsatisfiedRequirement):
        assert injector.get(IContext)

    async with injector.create_asgi_args() as request_provider:
        # resolving RequestScope during request will behave like singleton
        assert request_provider.get(IContext) == request_provider.get(IContext)
        assert isinstance(injector.get(IContext), AnyContext)


def test_invalid_use_of_provider_config():
    with pytest.raises(DIImproperConfiguration):
        ProviderConfig(IContext, use_class=AnyContext, use_value=AnyContext())


def test_provider_config_use_value():
    injector = EllarInjector(auto_bind=False)
    ProviderConfig(IContext, use_value=AnyContext()).register(injector.container)

    # IContext is now registered as a singleton
    assert injector.get(IContext) == injector.get(IContext)


def test_provider_config():
    injector = EllarInjector(auto_bind=False)
    ProviderConfig(TransientRequestContext).register(injector.container)

    assert injector.get(TransientRequestContext) != injector.get(
        TransientRequestContext
    )  # RequestScope


def test_invalid_use_provider_config():
    injector = EllarInjector(auto_bind=False)
    any_ctx = AnyContext()
    with pytest.raises(DIImproperConfiguration) as ex:
        ProviderConfig(any_ctx).register(injector.container)

    assert (
        str(ex.value)
        == f"couldn't determine provider setup for {any_ctx}. Please use `ProviderConfig` or `register_services` function in a Module to configure the provider"
    )


def test_has_binding_works():
    @inject
    def inject_function(a: IContext):
        pass

    assert has_binding(IContext) is False
    assert has_binding(AnyContext) is True

    assert has_binding(lambda n: print("Hello")) is False
    assert has_binding(inject_function) is True
