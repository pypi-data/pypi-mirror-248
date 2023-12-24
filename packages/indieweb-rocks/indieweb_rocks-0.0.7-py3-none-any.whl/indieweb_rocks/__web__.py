"""IndieWeb.Rocks web app."""

import collections
import hashlib
import os

import easyuri
import micropub
import web
from web import tx

from indieweb_rocks import agent, app, refresh_domain, sites_path

from .utils import silos


@app.control("")
class Landing:
    """Site landing."""

    def get(self):
        """Return a search box and short description."""
        return app.view.landing()


@app.control("bot")
class Bot:
    """Site bot."""

    def get(self):
        """Return ."""
        web.header("Content-Type", "text/html")
        return "This site uses a bot with <code>User-Agent: IndieWebRocksBot</code>"


@app.control("featured")
class Featured:
    """Featured sites."""

    def get(self):
        """Return a list of sites with high test scores."""
        return app.view.featured()


@app.control("silos")
class Silos:
    """."""

    def get(self):
        """."""
        return app.view.silos()


@app.control("silos/url_summaries.json")
class SiloSummaries:
    """."""

    def get(self):
        """."""
        web.header("Content-Type", "application/json")
        return silos


@app.control("features")
class Features:
    """Features of sites."""

    def get(self):
        """Return a list of features and sites that support them."""
        return app.view.features()


@app.control("screens")
class Screens:
    """Site screenshots."""

    def get(self):
        """Return a list of site screenshots."""
        urls = [url for url in app.model.get_people()]
        return app.view.screens(urls)


@app.control("the-street")
class TheStreet:
    """The Street."""

    def get(self):
        """Return a list of ."""
        subdomains = collections.defaultdict(list)
        for url in app.model.get_people():
            url = easyuri.parse(url)
            domain = subdomains[f"{url.domain}.{url.suffix}"]
            if url.subdomain:
                domain.append(url.subdomain)
        domains = sorted(
            [
                (hashlib.sha256(d.encode("utf-8")).hexdigest().upper(), d)
                for d in subdomains
            ]
        )
        return app.view.the_street(domains, subdomains)


@app.control("search")
class Search:
    """Search the IndieWeb."""

    def get(self):
        """Return a query's results."""
        try:
            query = web.form("q").q
        except web.BadRequest:
            raise web.SeeOther("/search")
        try:
            url = easyuri.parse(query)
        except (ValueError, easyuri.SuffixNotFoundError):
            pass
        else:
            if url.suffix:
                raise web.SeeOther(f"/{url.minimized}")
        # people = tx.db.select(
        #     "people", where="url LIKE ? OR name LIKE ?", vals=[f"%{query}%"] * 2
        # )
        people = tx.db.select(
            "resources",
            what="json_extract(resources.details, '$.card') AS card",
            where="json_extract(resources.details, '$.card.name') LIKE ?",
            vals=[f"%{query}%"],
        )
        posts = tx.db.select(
            "resources",
            # what="json_extract(resources.details, '$.card')",
            where="json_extract(resources.details, '$.card.name') LIKE ?",
            vals=[f"%{query}%"],
        )
        return app.view.results(query, people, posts)


@app.control("posts")
class Posts:
    """Show indexed posts."""

    def get(self):
        """Return a chronological list of posts."""
        return app.view.posts(app.model.get_posts())


@app.control("people")
class People:
    """Show indexed people and organizations."""

    def get(self):
        """Return an alphabetical list of people and organizations."""
        return app.view.people(app.model.get_people())


@app.control("people.txt")
class PeopleTXT:
    """Index of people as plaintext."""

    def get(self):
        """Return a list of indexed sites."""
        # TODO # accept a
        # TODO tx.db.select(
        # TODO     tx.db.subquery(
        # TODO         "crawls", where="url not like '%/%'", order="crawled desc"
        # TODO     ),
        # TODO     group="url",
        # TODO )
        return "\n".join([url for url in app.model.get_people()])


@app.control("places")
class Places:
    """Show indexed places."""

    def get(self):
        """Return an alphabetical list of places."""
        return "places"


@app.control("events")
class Events:
    """Show indexed events."""

    def get(self):
        """Return a chronological list of events."""
        return "events"


@app.control("recipes")
class Recipes:
    """Show indexed recipes."""

    def get(self):
        """Return a list of recipes."""
        return ""


@app.control("reviews")
class Reviews:
    """Show indexed reviews."""

    def get(self):
        """Return a list of reviews."""
        return "reviews"


@app.control("projects")
class Projects:
    """Show indexed projects."""

    def get(self):
        """Return a list of projects."""
        return "projects"


@app.control("categories")
class Categories:
    """Browse by category."""

    def get(self):
        """Return an alphabetical list of categories."""
        return app.view.categories(app.model.get_categories())


@app.control("micropub")
class Micropub:
    """Proxy a Micropub request to the signed in user's endpoint."""

    def post(self):
        form = web.form()
        client = micropub.Client(tx.user.session["micropub_endpoint"])
        permalink = client.create_post(form)
        raise web.SeeOther(permalink)


@app.control("crawler")
class Crawler:
    """Crawler."""

    def get(self):
        """Return a log of crawls and form to post a new one."""
        return app.view.crawler()  # tx.db.select("crawls"))

    def post(self):
        urls = web.form("url").url.splitlines()
        for url in urls:
            web.enqueue(refresh_domain, url)
        raise web.Accepted(f"enqueued {len(urls)}")


@app.control("crawler/all")
class RecrawlAll:
    """Recrawl all people."""

    def post(self):
        for person in tx.db.select("people"):
            web.enqueue(refresh_domain, person["url"])
        raise web.Accepted("enqueued")


@app.control("stats")
class Stats:
    """Show stats."""

    def get(self):
        """Return site/IndieWeb statistics."""
        properties = collections.Counter()
        for person in app.model.get_people_details():
            for prop in person["details"]:
                properties[prop] += 1
        return app.view.stats(properties)


@app.control("sites")
class Sites:
    """Index of sites as HTML."""

    def get(self):
        """Return a list of indexed sites."""
        # TODO # accept a
        # TODO tx.db.select(
        # TODO     tx.db.subquery(
        # TODO         "crawls", where="url not like '%/%'", order="crawled desc"
        # TODO     ),
        # TODO     group="url",
        # TODO )
        with tx.db.transaction as cur:
            urls = cur.cur.execute(
                " select * from ("
                + "select * from crawls where url not like '%/%' order by crawled desc"
                + ") group by url"
            )
        return app.view.sites(urls)


@app.control("sites.txt")
class SitesTXT:
    """Index of sites as plaintext."""

    def get(self):
        """Return a list of indexed sites."""
        # TODO # accept a
        # TODO tx.db.select(
        # TODO     tx.db.subquery(
        # TODO         "crawls", where="url not like '%/%'", order="crawled desc"
        # TODO     ),
        # TODO     group="url",
        # TODO )
        with tx.db.transaction as cur:
            urls = cur.cur.execute(
                " select * from ("
                + "select * from crawls where url not like '%/%' order by crawled desc"
                + ") group by url"
            )
        return "\n".join([url[0] for url in urls])


@app.control("commons")
class Commons:
    """"""

    def get(self):
        return app.view.commons()


@app.control("robots.txt")
class RobotsTxt:
    """"""

    def get(self):
        return "User-agent: *\nDisallow: /"


@app.control("terms")
class TermsOfService:
    """Terms of service."""

    def get(self):
        """Return a terms of service."""
        return app.view.terms()


@app.control("privacy")
class PrivacyPolicy:
    """Privacy policy."""

    def get(self):
        """Return a privacy policy."""
        subprocess.run(["notify-send", "-u", "critical", "PRIVACY POLICY"])
        return app.view.privacy()


@app.control("map")
class Map:
    """Map view."""

    def get(self):
        """Render a map view."""
        return app.view.map()


@app.control("toolbox")
class Toolbox:
    """Tools."""

    def get(self):
        """Display tools."""
        return app.view.toolbox()


@app.control("toolbox/representative-card")
class RepresentativeCard:
    """Representative card tool."""

    def get(self):
        """Parse representative card."""
        try:
            url = web.form("url").url
        except web.BadRequest:
            return app.view.toolbox.representative_card()
        web.header("Content-Type", "application/json")
        return web.dump(agent.get(url).card.data, indent=2)


@app.control("toolbox/representative-feed")
class RepresentativeFeed:
    """Representative feed tool."""

    def get(self):
        """Parse representative feed."""
        try:
            url = web.form("url").url
        except web.BadRequest:
            return app.view.toolbox.representative_feed()
        web.header("Content-Type", "application/json")
        return web.dump(agent.get(url).feed.data, indent=2)


@app.control("indieauth")
class IndieAuth:
    """IndieAuth support."""

    def get(self):
        """Return sites with IndieAuth support."""
        sites = tx.db.select("resources", order="url ASC")
        # for site in sites:
        #     details = site["details"]
        #     if indieauth := details.get("indieauth"):
        #         domain = details["domain"]["name"]
        return app.view.indieauth(sites)


@app.control("details/{site}(/{page})?")
class SiteDetails:
    """A web resource."""

    def get(self, site, page=None):
        web.header("Content-Type", "application/json")
        return tx.db.select("resources", where="url = ?", vals=[site])[0]["details"]


@app.control("a11y/{site}(/{page})?")
class Accessibility:
    """A web resource."""

    def get(self, site, page=None):
        try:
            a11y = web.load(path=sites_path / site / "a11y.json")
        except FileNotFoundError:
            a11y = None
        return app.view.a11y(site, a11y)


# @app.control("{site}")
@app.control("{site}(/{page})?")
class URL:
    """A web resource."""

    def get(self, site, page=None):
        """Return a site analysis."""
        page_url = easyuri.parse(site)
        if page:
            page_url = easyuri.parse(f"{site}/{page}")
        redirect = tx.db.select(
            "redirects",
            what="outgoing",
            where="incoming = ?",
            vals=[page_url.minimized],
        )
        try:
            raise web.SeeOther(redirect[0]["outgoing"])
        except IndexError:
            pass
        if page:
            return app.view.page(page_url, {})
        try:
            details = tx.db.select("resources", where="url = ?", vals=[site])[0][
                "details"
            ]
            # XXX web.load(path=sites_path / site / "details.json")
        except IndexError:
            web.enqueue(refresh_domain, site)
            return app.view.crawl_enqueued()
        if site in [s[0] for s in silos.values()]:
            return app.view.silo(page_url, details)
        try:
            audits = web.load(path=sites_path / site / "audits.json")
        except FileNotFoundError:
            audits = None
        try:
            a11y = web.load(path=sites_path / site / "a11y.json")
        except FileNotFoundError:
            a11y = None
        try:
            manifest = web.load(path=sites_path / site / "manifest.json")
        except FileNotFoundError:
            manifest = None
        return app.view.site(page_url, details, audits, a11y, manifest)

    def post(self, site):
        web.enqueue(refresh_domain, site)
        return app.view.crawl_enqueued()
        # TODO
        # if no-flash-header or use form argument:
        #     raise web.SeeOther(); flash user's session with message to insert as CSS
        # elif flash-header:
        #     return just message as JSON
        raise web.flash("crawl enqueued")


@app.control("sites/{site}/screenshot.png")
class SiteScreenshot:
    """A site's screenshot."""

    def get(self, site):
        """Return a PNG document rendering given site's screenshot."""
        if os.getenv("WEBCTX") == "dev":
            return sites_path / site / "screenshot.png"
        web.header("Content-Type", "image/png")
        web.header("X-Accel-Redirect", f"/data/{site}/screenshot.png")


@app.control("sites/{site}/scoreboard.svg")
class SiteScoreboard:
    """A site's scoreboard."""

    def get(self, site):
        """Return an SVG document rendering given site's scoreboard."""
        if os.getenv("WEBCTX") == "dev":
            return sites_path / site / "scoreboard.svg"
        web.header("Content-Type", "image/svg+xml")
        web.header("X-Accel-Redirect", f"/data/{site}/scoreboard.svg")
