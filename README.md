# coframe-commons

Shared, reusable [Coframe](https://github.com/claudiodriussi/coframe) plugins —
the parts that nearly every management application needs, kept out of both the
framework core and any individual customer app.

The core is *mechanism*: it knows how to turn YAML into models, queries and UI.
This repository is *policy*: what a user is, what a business partner is, which
types are worth having. The two churn at different rates and for different
reasons, which is why they are separate repositories.

## Layout

```
plugins/          the shared root — one directory per subject, each a plugin
  common/           reusable types (ID, Money, Address, Archivable…) + Config
  users/            User, UserLog
demo/             reference app: the only consumer shipped with the plugins
```

`plugins/` is a plugin **root** in the Coframe sense: every directory below it
holding a `config.yaml` is a plugin, and plugins never nest. `demo/` sits
outside the root on purpose — its own `config.yaml` is an *app* config, and a
root only ever contains plugins.

Boundaries between subjects are enforced by `depends_on:` in each plugin's
`config.yaml`, not by repository boundaries. If a subject ever outgrows this
repository, `git subtree split --prefix=plugins/<name>` extracts it with its
history intact.

## Using the plugins from an application

A plugin root can live anywhere: list it in the app's `config.yaml`, relative
to the app directory. Name what you want from it — dependencies come along, so
`include: [partners]` also brings `common`.

```yaml
plugins:
  - path: ../../commons/plugins
    include: [users, partners]
  - plugins                        # your own root, taken whole
```

Selection is positive by design: plugins added to this repository later stay
inert until an application asks for them by name. Taking the whole root — the
bare-path form — is fine for a root you own, and means your application gains
whatever this repository gains, tables included.

Order matters only for `deep_merge` precedence; dependency order is resolved
from `depends_on:`.

Plugins that ship a query behavior must have it registered by the app, so the
core stays agnostic:

```python
from common.model import Archivable
app.add_query_behavior(Archivable)
```

## The demo app

`demo/` exists so the shared plugins have somewhere to be exercised and shown
without dragging in a real customer application. It points at `../plugins` the
same way an external app would.

```bash
cd demo && python demo.py        # generates model.py, creates the DB, smoke test
```

Dev credentials: `admin` / `admin`. It expects the coframe checkout as a
sibling of this repository; set `COFRAME_PATH` if it lives elsewhere.

## License

MIT — see [LICENSE](LICENSE).
