#!/bin/bash

scrapy crawl dev_loader -a fecha_desde=01/02/2022 -a fecha_hasta=02/02/2022 -a competencia_id=2 -corte_id
