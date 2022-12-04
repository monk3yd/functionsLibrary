import json
import scrapy


class IdMapConstructor(scrapy.Spider):
    name = "id_map_constructor"
    allowed_domains = ["pjud.cl", "google.com"]
    start_urls = ["https://google.com"]

    def __init__(self):
        self.tipo_busqueda_id = 1
        self.competencia_id = 2
        self.corte_id = 25
        self.era = 2022

    def parse(self, response):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }
        url_landing = "https://oficinajudicialvirtual.pjud.cl/home/index.php"
        yield scrapy.Request(
            url=url_landing,
            method="GET",
            headers=headers,
            callback=self.landing
        )

    def landing(self, response):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://oficinajudicialvirtual.pjud.cl/indexN.php",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        url_web_forms = "https://oficinajudicialvirtual.pjud.cl/consultaUnificada.php"
        yield scrapy.Request(
            url=url_web_forms,
            method="GET",
            headers=headers,
            callback=self.extract_competencia_y_tipo
        )

    def extract_competencia_y_tipo(self, response):
        # with open("raw_output.html", "w") as file:
        #     file.write(response.text)

        # Competencia
        self.all_competencias = []
        competencia_dropdown = response.css("select#competencia option")
        for option in competencia_dropdown:
            competencia = {
                "id": option.css("option").attrib["value"],
                "name": option.css("option::text").get()
            }
            self.all_competencias.append(competencia)

        # Tipo de busqueda
        self.all_tipo_busquedas = []
        tipo_busquedas_dropdown = response.css("select#conTipoBus option")
        for option in tipo_busquedas_dropdown:
            tipo_busqueda = {
                "id": option.css("option").attrib["value"],
                "name": option.css("option::text").get(),
            }
            self.all_tipo_busquedas.append(tipo_busqueda)

        # Next Request
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://oficinajudicialvirtual.pjud.cl",
            "Connection": "keep-alive",
            "Referer": "https://oficinajudicialvirtual.pjud.cl/indexN.php",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        body = f"tipoBusqueda={self.tipo_busqueda_id}"
        url = "https://oficinajudicialvirtual.pjud.cl/combosJSON/leeCorte.php"
        yield scrapy.Request(
            url=url,
            method="POST",
            headers=headers,
            body=body,
            dont_filter=True,
            callback=self.extract_corte
        )

    def extract_corte(self, response):
        self.all_cortes = []
        for corte in response.json():
            corte = {
                "id": corte["COD_CORTE"],
                "name": corte["GLS_CORTE"]
            }
            self.all_cortes.append(corte)

        # Next Request
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://oficinajudicialvirtual.pjud.cl",
            "Connection": "keep-alive",
            "Referer": "https://oficinajudicialvirtual.pjud.cl/indexN.php",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        body = f"codCompetencia={self.competencia_id}&codCorte={self.corte_id}&codAnho={self.era}"
        url = "https://oficinajudicialvirtual.pjud.cl/ADIR_871/json/cmbTipos.php"
        yield scrapy.Request(
            url=url,
            method="POST",
            headers=headers,
            body=body,
            dont_filter=True,
            callback=self.extract_tipos
        )

    def extract_tipos(self, response):
        # with open("tipos.html", "a") as file:
        #     file.write(response.text)

        self.all_tipos = []
        options = response.css("option")
        for option in options:
            tipo = {
                "id": option.css("option").attrib["value"],
                "name": option.css("option::text").get()
            }
            self.all_tipos.append(tipo)

        id_map = {
            "competencias": self.all_competencias,
            "cortes": self.all_cortes,
            "tipos_causas": self.all_tipos,
            "tipos_busquedas": self.all_tipo_busquedas,
        }

        yield id_map

        with open("id_mapping.json", "a") as file:
            file.write(json.dumps(id_map, indent=4))
