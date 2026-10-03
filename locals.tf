# Valores comunes para nombrar y etiquetar los recursos del entorno QA,
# siguiendo las abreviaturas recomendadas por Microsoft (rg, log, appi, asp).
locals {
  location = "mexicocentral"
  suffix   = "utvt-integradora-qa-mxc-lgg01"

  tags = {
    project     = "utvt-integradora"
    environment = "qa"
    owner       = "Ludwin Garcia Gaytan"
    managed_by  = "terraform"
  }
}
