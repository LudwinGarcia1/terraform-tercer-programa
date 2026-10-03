# Tercer programa de Terraform

Práctica de Terraform basada en el laboratorio
[`tercer-programa`](https://github.com/jorgealmeidamontiel/terraform-laboratories/tree/main/tercer-programa).

Despliega en Azure la infraestructura de un entorno QA para una aplicación web Node.js,
con su monitoreo centralizado.

## Recursos

| Recurso | Nombre | Descripción |
|---|---|---|
| `azurerm_resource_group` | `rg-utvt-integradora-qa-mxc-lgg01` | Agrupa todos los recursos del entorno QA |
| `azurerm_log_analytics_workspace` | `log-utvt-integradora-qa-mxc-lgg01` | Registros con retención de 30 días y cuota de 0.1 GB/día |
| `azurerm_application_insights` | `appi-utvt-integradora-qa-mxc-lgg01` | Telemetría de la aplicación, conectada a Log Analytics |
| `azurerm_service_plan` | `asp-utvt-integradora-qa-mxc-lgg01` | Plan Linux en capa gratuita (`F1`) |
| `azurerm_linux_web_app` | `app-utvt-integradora-web-qa-mxc-lgg01` | Web App Node.js 24 LTS, solo HTTPS y TLS 1.2 mínimo |

Los nombres siguen las
[abreviaturas recomendadas por Microsoft](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations).

## Estructura

| Archivo | Descripción |
|---|---|
| `providers.tf` | Bloque `terraform` y proveedor `hashicorp/azurerm` |
| `variables.tf` | Variables de entrada (suscripción, SKU, versión de Node, nombre de la Web App) |
| `locals.tf` | Región, sufijo de nombres y etiquetas comunes |
| `main.tf` | Recursos de Azure |
| `outputs.tf` | Valores de salida (grupo de recursos, URL de la Web App, monitoreo) |
| `terraform.tfvars.example` | Plantilla para indicar el ID de la suscripción |

## Requisitos

- Terraform `>= 1.9.0` (probado con v1.16.2)
- Azure CLI con una sesión iniciada (`az login`)

## Ejecución

```bash
az login
cp terraform.tfvars.example terraform.tfvars   # Colocar el ID de la suscripción
terraform init
terraform validate
terraform plan -out tfplan
terraform apply tfplan
terraform output
terraform destroy                              # Elimina los recursos al terminar
```

`terraform.tfvars` y los archivos de estado están en `.gitignore` para no publicar el ID de la
suscripción ni datos de la infraestructura.
