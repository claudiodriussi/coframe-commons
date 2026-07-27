"""commons demo harness — loads the shared plugins and exercises them.

Slim analogue of coframe's devtest.py: loads the plugin root, computes the DB
schema, regenerates model.py, initialises the sqlite DB and runs a smoke test.

Run from this directory:  python demo.py
"""
import sys
from pathlib import Path

# Reach the coframe library package. This repo is a sibling of the coframe
# checkout in the development workspace; override with COFRAME_PATH when it
# lives somewhere else.
import os  # noqa: E402
_lib = os.environ.get("COFRAME_PATH", "../../coframe")
sys.path.append(str(Path(_lib).resolve()))

import coframe  # noqa: E402
import coframe.plugins  # noqa: E402
import coframe.utils  # noqa: E402
import coframe.source  # noqa: E402


def setup(generate: bool = True):
    """Load plugins, compute schema, register behaviors, (re)generate model.py."""
    plugins = coframe.plugins.PluginsManager()
    plugins.load_config("config.yaml")
    coframe.utils.register_standard_handlers(plugins)
    plugins.load_plugins()

    app = coframe.utils.get_app()
    app.calc_db(plugins)

    # Commons Archivable query behavior — injected, core stays agnostic (GL-19).
    from common.model import Archivable  # type: ignore
    app.add_query_behavior(Archivable)

    if generate:
        model_file = "model.py"
        if plugins.should_regenerate(model_file):
            print("Generating model.py ...")
            coframe.source.Generator(app).generate(filename=model_file)
        else:
            print("model.py up to date.")

    return app, plugins


def seed(app, model):
    """Create the admin user on an empty database (dev credentials: admin/admin)."""
    with app.get_session() as session:
        if session.query(model.User).first():
            return
        session.add(model.User(
            name="Administrator",
            username="admin",
            password="admin",
            email="admin@example.com",
            is_admin=True,
        ))
        session.commit()


def main():
    app, plugins = setup()

    import model  # type: ignore  # generated
    app.initialize_db(plugins.config["db_engine"], model)
    plugins.load_all_locales()
    seed(app, model)

    print(f"Plugins caricati: {', '.join(plugins.sorted)}")
    print(f"Tabelle: {', '.join(sorted(app.tables.keys()))}")

    with app.get_session() as session:
        for user in session.query(model.User).all():
            print(f"User {user.id}: {user.username} <{user.email}> admin={user.is_admin}")
        print(f"Config rows: {session.query(model.Config).count()}")

    print("commons demo smoke OK")


if __name__ == "__main__":
    main()
