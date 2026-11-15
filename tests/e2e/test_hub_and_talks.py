"""
Archivo: tests/e2e/test_hub_and_talks.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida de extremo a extremo (E2E) en Chromium headless el sitio estático compilado
del Hub Selector y las dos charlas reales (`2026-forecasting-ia` y `2026-falsa-alarma`)
mediante un servidor HTTP efímero levantado sobre un directorio temporal aislado.

Acciones Principales:
    - Compila el sitio completo con `build_all` hacia `tmp_path_factory` (`base_path="/"`).
    - Levanta un `ThreadingHTTPServer` en `127.0.0.1:0` y verifica respuestas HTTP 200.
    - Simula el recorrido real de usuario en Playwright: búsqueda, filtros,
      Modo Presentador, modal Config y navegación de diapositivas en ambas charlas.
    - Exige cero errores `pageerror` y cero respuestas HTTP >= 400 en `127.0.0.1`.

Estructura Interna:
    - `_QuietSimpleHTTPRequestHandler`: Manejador HTTP estático sin ruido en stderr.
    - `_find_cached_chromium_executable`: Localiza binarios cacheados de Chromium si faltan los exactos.
    - `_launch_chromium`: Inicia Chromium headless de Playwright con respaldo local.
    - `built_site_server`: Fixture de módulo que compila `_site` y sirve `127.0.0.1:0`.
    - `test_ephemeral_http_server_serves_hub_index`: Prueba unitaria del servidor efímero.
    - `test_user_e2e_hub_filters_and_both_talks`: Simulación E2E completa en Chromium.

Entradas / Dependencias:
    - `scripts.build_all.build_all`, directorio real `talks/` y `playwright.sync_api`.

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de la Tarea T3.2.1.

Ejemplo de Integración:
    python -m pytest tests/e2e/test_hub_and_talks.py -v
"""

from collections.abc import Iterator
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import threading
import urllib.request

from playwright.sync_api import Browser, Error as PlaywrightError, Playwright, expect, sync_playwright
import pytest

from scripts.build_all import build_all

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
LOCAL_HOST: str = "127.0.0.1"
HTTP_TIMEOUT_SECONDS: int = 10


class _QuietSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Sirve archivos estáticos omitiendo el registro de trazas HTTP en stderr.
    """

    def log_message(self, format: str, *args: object) -> None:
        """
        Suprime los logs de acceso por petición para mantener limpia la salida de pytest.

        Args:
            format (str): Cadena de formato estándar de `BaseHTTPRequestHandler`.
            *args (object): Argumentos posicionales del mensaje de log.
        """
        _ = (format, args)


def _find_cached_chromium_executable() -> Path | None:
    """
    Busca un ejecutable headless de Chromium cacheado en el directorio de Playwright.

    Returns:
        Path | None: Ruta al binario encontrado o `None` si no existe ninguno en caché.
    """
    cache_candidates: list[Path] = []
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        cache_candidates.append(Path(local_app_data) / "ms-playwright")
    cache_candidates.append(Path.home() / ".cache" / "ms-playwright")

    executable_patterns = (
        "chromium_headless_shell-*/**/chrome-headless-shell.exe",
        "chromium_headless_shell-*/**/headless_shell.exe",
        "chromium_headless_shell-*/**/chrome-headless-shell",
        "chromium-*/**/chrome.exe",
        "chromium-*/**/chrome",
    )

    for cache_dir in cache_candidates:
        if not cache_dir.is_dir():
            continue
        for pattern in executable_patterns:
            matches = sorted(cache_dir.glob(pattern), reverse=True)
            for match in matches:
                if match.is_file():
                    return match
    return None


def _launch_chromium(playwright: Playwright) -> Browser:
    """
    Lanza Chromium headless usando el binario estándar de Playwright o un respaldo local.

    Args:
        playwright (Playwright): Instancia activa de `sync_playwright`.

    Returns:
        Browser: Instancia de navegador Chromium lista para crear contextos y páginas.
    """
    try:
        return playwright.chromium.launch(headless=True)
    except PlaywrightError:
        cached_executable = _find_cached_chromium_executable()
        if cached_executable is not None:
            return playwright.chromium.launch(
                headless=True,
                executable_path=str(cached_executable),
            )
        for channel in ("chrome", "msedge"):
            try:
                return playwright.chromium.launch(headless=True, channel=channel)
            except PlaywrightError:
                continue
        raise


@pytest.fixture(scope="module")
def built_site_server(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """
    Compila el Hub y ambas charlas en un directorio temporal y levanta un servidor HTTP efímero.

    Args:
        tmp_path_factory (pytest.TempPathFactory): Fábrica de directorios temporales de pytest.

    Yields:
        str: URL base del servidor local (ej. `http://127.0.0.1:54321`).
    """
    tmp_site = tmp_path_factory.mktemp("e2e_site")
    build_all(talks_dir=REPO_ROOT / "talks", out_dir=tmp_site, base_path="/")

    handler_factory = functools.partial(
        _QuietSimpleHTTPRequestHandler,
        directory=str(tmp_site),
    )
    server = ThreadingHTTPServer((LOCAL_HOST, 0), handler_factory)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        yield f"http://{LOCAL_HOST}:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=5)


def test_ephemeral_http_server_serves_hub_index(built_site_server: str) -> None:
    """
    Valida que el servidor efímero responde HTTP 200 en el Hub, catálogo JSON y ambas charlas.
    """
    expected_paths = (
        "/",
        "/talks.json",
        "/2026-sdd-proyectos-reales/",
        "/2026-forecasting-ia/",
        "/2026-falsa-alarma/",
    )

    for route in expected_paths:
        url = f"{built_site_server}{route}"
        with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_SECONDS) as response:
            assert response.status == 200, f"Respuesta inesperada en {url}: {response.status}"
            body = response.read().decode("utf-8")
            assert len(body) > 0

    with urllib.request.urlopen(
        f"{built_site_server}/talks.json",
        timeout=HTTP_TIMEOUT_SECONDS,
    ) as catalog_response:
        catalog = json.loads(catalog_response.read().decode("utf-8"))
        slugs = [talk["slug"] for talk in catalog["talks"]]
        assert slugs == [
            "2026-sdd-proyectos-reales",
            "2026-forecasting-ia",
            "2026-falsa-alarma",
        ]


def test_user_e2e_hub_filters_and_both_talks(built_site_server: str) -> None:
    """
    Simula la interacción completa de usuario en Chromium sobre el Hub y ambas charlas reales.
    """
    page_errors: list[str] = []
    failed_responses: list[str] = []

    def _record_failed_response(response: object) -> None:
        # Filtra por host local para evitar falsos fallos por fuentes externas sin red.
        url = getattr(response, "url", "")
        status = getattr(response, "status", 0)
        if LOCAL_HOST in url and status >= 400:
            failed_responses.append(f"{status} {url}")

    with sync_playwright() as playwright:
        browser = _launch_chromium(playwright)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))
        page.on("response", _record_failed_response)

        try:
            # 1. Carga el Hub Selector y valida marca personal y ausencia de badge ajeno.
            page.goto(f"{built_site_server}/", wait_until="domcontentloaded")
            expect(page.locator("h1.hub-title")).to_contain_text("Alex Prieto Romani")
            assert "Alex Prieto Romani" in page.title()
            assert "data_wizard_badge" not in page.content()
            assert page.locator('[src*="data_wizard_badge"]').count() == 0

            visible_cards = page.locator("#talksGrid .talk-card:visible")
            expect(visible_cards).to_have_count(3)

            # 2. Valida búsqueda de texto en tiempo real y limpieza del campo.
            search_input = page.locator("#searchInput")
            search_input.fill("falsa")
            expect(visible_cards).to_have_count(1)
            search_input.fill("")
            expect(visible_cards).to_have_count(3)

            # 3. Valida filtros de motor (Astro, Python Deck y Todas).
            page.locator('#filterPills .pill[data-filter="astro"]').click()
            expect(visible_cards).to_have_count(1)
            page.locator('#filterPills .pill[data-filter="python-deck"]').click()
            expect(visible_cards).to_have_count(2)
            page.locator('#filterPills .pill[data-filter="all"]').click()
            expect(visible_cards).to_have_count(3)

            # 4. Activa Modo Presentador y abre/cierra el modal { } Config.
            presenter_btn = page.locator("#presenterBtn")
            presenter_btn.click()
            expect(presenter_btn).to_have_attribute("aria-pressed", "true")
            expect(page.locator(".presenter-bar").first).to_be_visible()

            page.locator(
                '.talk-card[data-slug="2026-forecasting-ia"] button[data-action="config"]'
            ).click()
            modal_backdrop = page.locator("#modalBackdrop")
            expect(modal_backdrop).to_have_class(re.compile(r"\bopen\b"))
            modal_json_text = page.locator("#modalBody").inner_text()
            assert '"slug"' in modal_json_text
            assert '"2026-forecasting-ia"' in modal_json_text
            page.locator("#modalCloseBtn").click()
            expect(modal_backdrop).not_to_have_class(re.compile(r"\bopen\b"))

            # 5. Navega a 2026-forecasting-ia desde su botón Presentar.
            page.locator(
                '.talk-card[data-slug="2026-forecasting-ia"] a.btn-primary'
            ).click()
            page.wait_for_load_state("domcontentloaded")
            expect(page.locator(".slide.active")).to_have_attribute("data-index", "1")
            expect(page.locator("#slideIndicator")).to_have_text("01 / 31")

            page.keyboard.press("ArrowRight")
            expect(page.locator(".slide.active")).to_have_attribute("data-index", "2")
            expect(page.locator("#slideIndicator")).to_have_text("02 / 31")

            page.keyboard.press("n")
            expect(page.locator("#speakerDrawer")).to_have_class(re.compile(r"\bopen\b"))
            assert page.evaluate("typeof window.Chart !== 'undefined'") is True

            # 6. Regresa al Hub y navega a 2026-falsa-alarma desde su botón Presentar.
            page.goto(f"{built_site_server}/", wait_until="domcontentloaded")
            page.locator(
                '.talk-card[data-slug="2026-falsa-alarma"] a.btn-primary'
            ).click()
            page.wait_for_load_state("domcontentloaded")

            expect(page.locator(".slide.active h1")).to_contain_text(
                "Falsa alarma o amenaza real"
            )
            expect(page.locator("#curNum")).to_have_text("1")

            page.keyboard.press("ArrowRight")
            expect(page.locator("#curNum")).to_have_text("2")
            expect(page.locator("#kpiBar")).to_be_visible()
            expect(page.locator("#deck")).to_be_visible()
            expect(page.locator("#kpi-acc")).not_to_be_empty()

            # 7. Regresa al Hub y navega a 2026-sdd-proyectos-reales.
            page.goto(f"{built_site_server}/", wait_until="domcontentloaded")
            page.locator(
                '.talk-card[data-slug="2026-sdd-proyectos-reales"] a.btn-primary'
            ).click()
            page.wait_for_load_state("domcontentloaded")
            expect(page.locator(".slide.active")).to_have_attribute("data-index", "1")
            page.keyboard.press("ArrowRight")
            expect(page.locator(".slide.active")).to_have_attribute("data-index", "2")
            page.keyboard.press("n")
            assert page.evaluate("typeof window.Chart !== 'undefined'") is True
        finally:
            context.close()
            browser.close()

    assert page_errors == [], f"Se detectaron errores JS en página: {page_errors}"
    assert failed_responses == [], (
        f"Se detectaron respuestas HTTP >= 400 en localhost: {failed_responses}"
    )
