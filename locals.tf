# Valores comunes para nombrar y etiquetar los recursos del entorno QA,
# siguiendo las abreviaturas recomendadas por Microsoft (rg, log, appi, asp).
# Se utiliza la región 'eastus' (abreviatura CAF: 'use') autorizada para la suscripción educativa.
locals {
  location = "eastus"
  suffix   = "utvt-integradora-qa-use-lgg01"

  tags = {
    project     = "utvt-integradora"
    environment = "qa"
    owner       = "Ludwin Garcia Gaytan"
    managed_by  = "terraform"
  }
}
