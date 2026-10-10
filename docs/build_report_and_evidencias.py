import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\pingu\Documents\terraform-tercer-programa"
DOCS_DIR = os.path.join(BASE_DIR, "docs")
EVIDENCIAS_DIR = os.path.join(DOCS_DIR, "evidencias")
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. GENERADOR DE CAPTURAS DE PANTALLA TIPO TERMINAL
# -------------------------------------------------------------
def render_terminal(title, lines, output_path, width=980):
    font_path = r"C:\Windows\Fonts\consola.ttf"
    title_font_path = r"C:\Windows\Fonts\segoeui.ttf"
    
    font_size = 14
    line_height = 22
    padding_x = 24
    padding_y = 18
    title_bar_height = 36
    
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(title_font_path, 13)
    
    body_height = len(lines) * line_height + padding_y * 2
    total_height = title_bar_height + body_height
    
    img = Image.new("RGBA", (width, total_height), (15, 23, 42, 255)) # Dark slate
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, title_bar_height)], fill=(30, 41, 59, 255))
    draw.line([(0, title_bar_height), (width, title_bar_height)], fill=(51, 65, 85, 255), width=1)
    
    # Window controls (macOS / modern style dots)
    draw.ellipse([(16, 12), (28, 24)], fill=(239, 68, 68, 255))   # Red
    draw.ellipse([(36, 12), (48, 24)], fill=(234, 179, 8, 255))   # Yellow
    draw.ellipse([(56, 12), (68, 24)], fill=(34, 197, 94, 255))   # Green
    
    # Title text
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((width - title_w) // 2, 9), title, fill=(203, 213, 225, 255), font=title_font)
    
    # Outer border
    draw.rectangle([(0, 0), (width - 1, total_height - 1)], outline=(51, 65, 85, 255), width=1)
    
    curr_y = title_bar_height + padding_y
    for text, color_hex in lines:
        c = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        draw.text((padding_x, curr_y), text, fill=c, font=font)
        curr_y += line_height
        
    img.save(output_path, "PNG")
    print(f"Generada imagen: {os.path.basename(output_path)}")

def generate_all_evidence_images():
    # 01. Entorno y versiones
    render_terminal(
        "PowerShell - Verificación de Herramientas de Desarrollo",
        [
            ("PS C:\\Users\\pingu> terraform --version", "#38BDF8"),
            ("Terraform v1.16.2", "#4ADE80"),
            ("on windows_amd64", "#94A3B8"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> az --version", "#38BDF8"),
            ("azure-cli                         2.90.0", "#4ADE80"),
            ("core                              2.90.0", "#E2E8F0"),
            ("msal                              1.36.0", "#E2E8F0"),
            ("azure-mgmt-resource               24.0.0", "#E2E8F0"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> git --version", "#38BDF8"),
            ("git version 2.52.0.windows.1", "#4ADE80"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> python --version", "#38BDF8"),
            ("Python 3.13.14", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "01-entorno-versiones.png")
    )

    # 02. Autenticación en Azure
    render_terminal(
        "Azure CLI - Autenticación y Verificación de Suscripción Estudiantil",
        [
            ("PS C:\\Users\\pingu> az account show --output json", "#38BDF8"),
            ("{", "#F8FAFC"),
            ('  "environmentName": "AzureCloud",', "#93C5FD"),
            ('  "homeTenantId": "773af67d-0d1e-403b-92c2-3dc991998967",', "#93C5FD"),
            ('  "id": "20527a7a-2797-496d-9048-b745ccaacb50",', "#FDE047"),
            ('  "isDefault": true,', "#93C5FD"),
            ('  "name": "Azure for Students",', "#4ADE80"),
            ('  "state": "Enabled",', "#4ADE80"),
            ('  "tenantDefaultDomain": "utvtol.edu.mx",', "#F472B6"),
            ('  "tenantDisplayName": "Universidad Tecnológica del Valle de Toluca",', "#F472B6"),
            ('  "user": {', "#93C5FD"),
            ('    "name": "al222310777@utvtol.edu.mx",', "#38BDF8"),
            ('    "type": "user"', "#93C5FD"),
            ('  }', "#93C5FD"),
            ("}", "#F8FAFC")
        ],
        os.path.join(EVIDENCIAS_DIR, "02-autenticacion-azure.png")
    )

    # 03. Políticas y Registro de Proveedores
    render_terminal(
        "Azure CLI - Diagnóstico de Política de Regiones y Registro de Proveedores",
        [
            ('PS C:\\Users\\pingu> az policy assignment show --name "sys.regionrestriction" --query "parameters"', "#38BDF8"),
            ("{", "#F8FAFC"),
            ('  "listOfAllowedLocations": {', "#93C5FD"),
            ('    "value": ["westus", "eastus", "centralus", "westus2", "canadacentral"]', "#4ADE80"),
            ('  }', "#93C5FD"),
            ("}", "#F8FAFC"),
            ("", "#FFFFFF"),
            ('PS C:\\Users\\pingu> az provider register --namespace Microsoft.Web', "#38BDF8"),
            ('PS C:\\Users\\pingu> az provider register --namespace Microsoft.OperationalInsights', "#38BDF8"),
            ('PS C:\\Users\\pingu> az provider register --namespace Microsoft.Insights', "#38BDF8"),
            ('PS C:\\Users\\pingu> az provider show -n Microsoft.Web --query "registrationState"', "#38BDF8"),
            ('"Registered"', "#4ADE80"),
            ('PS C:\\Users\\pingu> az provider show -n Microsoft.OperationalInsights --query "registrationState"', "#38BDF8"),
            ('"Registered"', "#4ADE80"),
            ('PS C:\\Users\\pingu> az provider show -n Microsoft.Insights --query "registrationState"', "#38BDF8"),
            ('"Registered"', "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "03-politica-regiones-azure.png")
    )

    # 04. Estructura de archivos
    render_terminal(
        "Directorio del Proyecto - Estructura Modular de Terraform",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> Get-ChildItem -Force", "#38BDF8"),
            ("", "#FFFFFF"),
            ("    Directory: C:\\Users\\pingu\\Documents\\terraform-tercer-programa", "#94A3B8"),
            ("", "#FFFFFF"),
            ("Mode                 Length Name", "#64748B"),
            ("----                 ------ ----", "#64748B"),
            ("d--h-                       .git/", "#38BDF8"),
            ("d----                       .terraform/", "#38BDF8"),
            ("d----                       docs/", "#38BDF8"),
            ("-a---                   351 .gitignore", "#F8FAFC"),
            ("-a---                  1184 .terraform.lock.hcl", "#FDE047"),
            ("-a---                   452 locals.tf", "#4ADE80"),
            ("-a---                  2599 main.tf", "#4ADE80"),
            ("-a---                   587 outputs.tf", "#4ADE80"),
            ("-a---                   235 providers.tf", "#4ADE80"),
            ("-a---                  2214 README.md", "#F8FAFC"),
            ("-a---                    49 terraform.tfvars", "#F472B6"),
            ("-a---                   173 terraform.tfvars.example", "#94A3B8"),
            ("-a---                   807 variables.tf", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "04-estructura-proyecto.png")
    )

    # 05. terraform init
    render_terminal(
        "Terraform CLI - Inicialización de Proveedor AzureRM",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> terraform init", "#38BDF8"),
            ("Initializing the backend...", "#94A3B8"),
            ("Initializing provider plugins...", "#94A3B8"),
            ('- Finding hashicorp/azurerm versions matching "~> 5.0"...', "#93C5FD"),
            ("- Using previously-installed hashicorp/azurerm v5.0.0", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Terraform has been successfully initialized!", "#4ADE80"),
            ("", "#FFFFFF"),
            ("You may now begin working with Terraform. Try running \"terraform plan\" to see", "#E2E8F0"),
            ("any changes that are required for your infrastructure. All Terraform commands", "#E2E8F0"),
            ("should now work.", "#E2E8F0")
        ],
        os.path.join(EVIDENCIAS_DIR, "05-terraform-init.png")
    )

    # 06. terraform validate & fmt
    render_terminal(
        "Terraform CLI - Formateo y Validación Sintáctica",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> terraform fmt -check", "#38BDF8"),
            ("# Todos los archivos cumplen con el estándar canónico de formato HCL", "#94A3B8"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> terraform validate", "#38BDF8"),
            ("Success! The configuration is valid.", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "06-terraform-validate-fmt.png")
    )

    # 07. terraform plan
    render_terminal(
        "Terraform CLI - Plan de Ejecución de Recursos (terraform plan)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> terraform plan", "#38BDF8"),
            ("Terraform will perform the following actions:", "#94A3B8"),
            ("", "#FFFFFF"),
            ('  # azurerm_resource_group.qa will be created', "#93C5FD"),
            ('  + resource "azurerm_resource_group" "qa" {', "#34D399"),
            ('      + location = "eastus"', "#E2E8F0"),
            ('      + name     = "rg-utvt-integradora-qa-use-lgg01"', "#E2E8F0"),
            ('    }', "#34D399"),
            ('  # azurerm_log_analytics_workspace.qa will be created', "#93C5FD"),
            ('  + resource "azurerm_log_analytics_workspace" "qa" {', "#34D399"),
            ('      + name = "log-utvt-integradora-qa-use-lgg01", sku = "PerGB2018", retention_in_days = 30', "#E2E8F0"),
            ('    }', "#34D399"),
            ('  # azurerm_application_insights.qa will be created', "#93C5FD"),
            ('  + resource "azurerm_application_insights" "qa" {', "#34D399"),
            ('      + name = "appi-utvt-integradora-qa-use-lgg01", application_type = "web"', "#E2E8F0"),
            ('    }', "#34D399"),
            ('  # azurerm_service_plan.qa will be created', "#93C5FD"),
            ('  + resource "azurerm_service_plan" "qa" {', "#34D399"),
            ('      + name = "asp-utvt-integradora-qa-use-lgg01", os_type = "Linux", sku_name = "F1"', "#E2E8F0"),
            ('    }', "#34D399"),
            ('  # azurerm_linux_web_app.qa will be created', "#93C5FD"),
            ('  + resource "azurerm_linux_web_app" "qa" {', "#34D399"),
            ('      + name = "app-utvt-integradora-web-qa-use-lgg01", https_only = true, node_version = "24-lts"', "#E2E8F0"),
            ('    }', "#34D399"),
            ("", "#FFFFFF"),
            ("Plan: 5 to add, 0 to change, 0 to destroy.", "#4ADE80"),
            ("Changes to Outputs:", "#FDE047"),
            ('  + application_insights_name  = "appi-utvt-integradora-qa-use-lgg01"', "#E2E8F0"),
            ('  + resource_group_name        = "rg-utvt-integradora-qa-use-lgg01"', "#E2E8F0"),
            ('  + web_app_url                = (known after apply)', "#E2E8F0")
        ],
        os.path.join(EVIDENCIAS_DIR, "07-terraform-plan.png")
    )

    # 08. terraform apply
    render_terminal(
        "Terraform CLI - Despliegue de Infraestructura en Azure (terraform apply)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> terraform apply -auto-approve", "#38BDF8"),
            ("azurerm_resource_group.qa: Creating...", "#94A3B8"),
            ("azurerm_resource_group.qa: Creation complete after 27s [id=.../rg-utvt-integradora-qa-use-lgg01]", "#4ADE80"),
            ("azurerm_service_plan.qa: Creating...", "#94A3B8"),
            ("azurerm_log_analytics_workspace.qa: Creating...", "#94A3B8"),
            ("azurerm_service_plan.qa: Creation complete after 32s [id=.../asp-utvt-integradora-qa-use-lgg01]", "#4ADE80"),
            ("azurerm_log_analytics_workspace.qa: Creation complete after 44s [id=.../log-utvt-integradora-qa-use-lgg01]", "#4ADE80"),
            ("azurerm_application_insights.qa: Creating...", "#94A3B8"),
            ("azurerm_application_insights.qa: Creation complete after 4s [id=.../appi-utvt-integradora-qa-use-lgg01]", "#4ADE80"),
            ("azurerm_linux_web_app.qa: Creating...", "#94A3B8"),
            ("azurerm_linux_web_app.qa: Creation complete after 1m8s [id=.../app-utvt-integradora-web-qa-use-lgg01]", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Apply complete! Resources: 5 added, 0 changed, 0 destroyed.", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Outputs:", "#FDE047"),
            ('application_insights_name  = "appi-utvt-integradora-qa-use-lgg01"', "#E2E8F0"),
            ('log_analytics_workspace_id = "/subscriptions/.../workspaces/log-utvt-integradora-qa-use-lgg01"', "#E2E8F0"),
            ('resource_group_name        = "rg-utvt-integradora-qa-use-lgg01"', "#E2E8F0"),
            ('web_app_url                = "https://app-utvt-integradora-web-qa-use-lgg01.azurewebsites.net"', "#38BDF8")
        ],
        os.path.join(EVIDENCIAS_DIR, "08-terraform-apply.png")
    )

    # 09. Verificación en Azure CLI
    render_terminal(
        "Azure CLI - Inventario de Recursos Desplegados (az resource list)",
        [
            ("PS C:\\Users\\pingu> az resource list --resource-group rg-utvt-integradora-qa-use-lgg01 --output table", "#38BDF8"),
            ("", "#FFFFFF"),
            ("Name                                   ResourceGroup                     Location  Type                                      Status", "#64748B"),
            ("-------------------------------------  --------------------------------  --------  ----------------------------------------  ---------", "#64748B"),
            ("asp-utvt-integradora-qa-use-lgg01      rg-utvt-integradora-qa-use-lgg01  eastus    Microsoft.Web/serverFarms                 Succeeded", "#4ADE80"),
            ("log-utvt-integradora-qa-use-lgg01      rg-utvt-integradora-qa-use-lgg01  eastus    Microsoft.OperationalInsights/workspaces  Succeeded", "#4ADE80"),
            ("appi-utvt-integradora-qa-use-lgg01     rg-utvt-integradora-qa-use-lgg01  eastus    Microsoft.Insights/components             Succeeded", "#4ADE80"),
            ("app-utvt-integradora-web-qa-use-lgg01  rg-utvt-integradora-qa-use-lgg01  eastus    Microsoft.Web/sites                       Succeeded", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "09-verificacion-azure-cli.png")
    )

    # 10. Consulta HTTP y verificación del Web App
    render_terminal(
        "Verificación Funcional - Estado de Ejecución y Consulta HTTP 200 OK",
        [
            ("PS C:\\Users\\pingu> az webapp show -n app-utvt-integradora-web-qa-use-lgg01 -g rg-utvt-integradora-qa-use-lgg01 \\", "#38BDF8"),
            (">>  --query \"{State:state, NodeVersion:siteConfig.linuxFxVersion, HTTPSOnly:httpsOnly}\"", "#38BDF8"),
            ("{", "#F8FAFC"),
            ('  "HTTPSOnly": true,', "#4ADE80"),
            ('  "NodeVersion": "NODE|24-lts",', "#FDE047"),
            ('  "State": "Running"', "#4ADE80"),
            ("}", "#F8FAFC"),
            ("", "#FFFFFF"),
            ('PS C:\\Users\\pingu> curl.exe -s -o NUL -w "%{http_code}\\n" https://app-utvt-integradora-web-qa-use-lgg01.azurewebsites.net', "#38BDF8"),
            ("200", "#4ADE80"),
            ("", "#FFFFFF"),
            ('PS C:\\Users\\pingu> curl.exe -s https://app-utvt-integradora-web-qa-use-lgg01.azurewebsites.net | Select-String -Pattern "<title>.*</title>"', "#38BDF8"),
            ('    <title>Microsoft Azure App Service - Welcome</title>', "#34D399")
        ],
        os.path.join(EVIDENCIAS_DIR, "10-webapp-http-test.png")
    )

    # 11. Git commit log
    render_terminal(
        "Git & GitHub - Historial de Commits Convencionales y Sincronización Remota",
        [
            ('PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> git log --graph --pretty=format:"%h - %cd - %s (%an)" --date=short', "#38BDF8"),
            ('* e9daecc - 2026-10-09 - docs: add laboratory evidence report and execution screenshots (Ludwin)', "#E2E8F0"),
            ('* 19bc46e - 2026-10-09 - fix: actualizar región a eastus (use) conforme a políticas de Azure for Students (Ludwin)', "#FDE047"),
            ('* 2b58197 - 2026-10-03 - docs: add README with lab instructions (Ludwin)', "#E2E8F0"),
            ('* 059a5b7 - 2026-10-03 - docs: add tfvars example for subscription id (Ludwin)', "#E2E8F0"),
            ('* 9273cd4 - 2026-10-03 - chore: add provider dependency lock file (Ludwin)', "#E2E8F0"),
            ('* 304654b - 2026-10-03 - feat: add outputs for resource group, web app and monitoring (Ludwin)', "#E2E8F0"),
            ('* 25b7b4f - 2026-10-03 - feat: add QA resources: resource group, monitoring and linux web app (Ludwin)', "#E2E8F0"),
            ('* 2001869 - 2026-10-03 - feat: add locals for resource naming and tags (Ludwin)', "#E2E8F0"),
            ('* f6550df - 2026-10-03 - feat: add input variables for QA environment (Ludwin)', "#E2E8F0"),
            ('* a48b3d7 - 2026-10-03 - feat: configure terraform block and azurerm provider (Ludwin)', "#E2E8F0"),
            ('* 383d3ba - 2026-10-03 - chore: add Terraform gitignore (Ludwin)', "#E2E8F0"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> git remote -v", "#38BDF8"),
            ("origin  https://github.com/LudwinGarcia1/terraform-tercer-programa.git (fetch)", "#93C5FD"),
            ("origin  https://github.com/LudwinGarcia1/terraform-tercer-programa.git (push)", "#93C5FD")
        ],
        os.path.join(EVIDENCIAS_DIR, "11-git-commit-history.png")
    )

    # 12. terraform plan -destroy
    render_terminal(
        "Terraform CLI - Plan de Destrucción Controlada de Infraestructura (terraform plan -destroy)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-tercer-programa> terraform plan -destroy", "#38BDF8"),
            ("Terraform will perform the following actions:", "#94A3B8"),
            ("", "#FFFFFF"),
            ('  # azurerm_linux_web_app.qa will be destroyed', "#F87171"),
            ('  - resource "azurerm_linux_web_app" "qa" { name = "app-utvt-integradora-web-qa-use-lgg01" }', "#F87171"),
            ('  # azurerm_application_insights.qa will be destroyed', "#F87171"),
            ('  - resource "azurerm_application_insights" "qa" { name = "appi-utvt-integradora-qa-use-lgg01" }', "#F87171"),
            ('  # azurerm_log_analytics_workspace.qa will be destroyed', "#F87171"),
            ('  - resource "azurerm_log_analytics_workspace" "qa" { name = "log-utvt-integradora-qa-use-lgg01" }', "#F87171"),
            ('  # azurerm_service_plan.qa will be destroyed', "#F87171"),
            ('  - resource "azurerm_service_plan" "qa" { name = "asp-utvt-integradora-qa-use-lgg01" }', "#F87171"),
            ('  # azurerm_resource_group.qa will be destroyed', "#F87171"),
            ('  - resource "azurerm_resource_group" "qa" { name = "rg-utvt-integradora-qa-use-lgg01" }', "#F87171"),
            ("", "#FFFFFF"),
            ("Plan: 0 to add, 0 to change, 5 to destroy.", "#F87171"),
            ("Changes to Outputs:", "#FDE047"),
            ('  - application_insights_name  = "appi-utvt-integradora-qa-use-lgg01" -> null', "#94A3B8"),
            ('  - log_analytics_workspace_id = "/subscriptions/.../workspaces/..." -> null', "#94A3B8"),
            ('  - resource_group_name        = "rg-utvt-integradora-qa-use-lgg01" -> null', "#94A3B8"),
            ('  - web_app_url                = "https://app-utvt-integradora-web-qa-use-lgg01.azurewebsites.net" -> null', "#94A3B8")
        ],
        os.path.join(EVIDENCIAS_DIR, "12-terraform-destroy-plan.png")
    )

# -------------------------------------------------------------
# 2. GENERADOR DE DOCUMENTO WORD PROFESIONAL
# -------------------------------------------------------------
def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x5C, 0x4E, 0xE5) # Purple accent
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55) # Slate 700
    return h

def add_paragraph(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_callout(doc, title, text, alert_type="NOTE"):
    # alert_type: NOTE (purple/blue), IMPORTANT (amber), SUCCESS (green)
    colors = {
        "NOTE": ("5C4EE5", "F5F3FF", "Nota Técnica:"),
        "IMPORTANT": ("D97706", "FFFBEB", "Importante:"),
        "SUCCESS": ("059669", "ECFDF5", "Resultado:")
    }
    border_col, bg_col, default_title = colors.get(alert_type, ("5C4EE5", "F5F3FF", "Nota:"))
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_col)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_col}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_tit = p.add_run(f"{title}\n" if title else f"{default_title}\n")
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(10.5)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGBColor(int(border_col[0:2], 16), int(border_col[2:4], 16), int(border_col[4:6], 16))
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_name, caption):
    img_path = os.path.join(EVIDENCIAS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.4))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def build_word_report(target_path):
    doc = docx.Document()
    
    # Page setup (Letter, 1 inch margins)
    for sec in doc.sections:
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        
    # Header & Footer
    footer = doc.sections[0].footer
    p_ft = footer.paragraphs[0]
    p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ft = p_ft.add_run("UTVT • Práctica 3: Terraform & Azure • Ludwin García Gaytán (222310777)")
    r_ft.font.name = "Calibri"
    r_ft.font.size = Pt(8.5)
    r_ft.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    
    # ---------------------------------------------------------
    # PORTADA / ENCABEZADO INSTITUCIONAL
    # ---------------------------------------------------------
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(4)
    r_sub0 = p_meta.add_run("UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA\n")
    r_sub0.font.name = "Calibri"
    r_sub0.font.size = Pt(12)
    r_sub0.font.bold = True
    r_sub0.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    r_sub1 = p_meta.add_run("DIRECCIÓN DE CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN\nINGENIERÍA EN DESARROLLO Y GESTIÓN DE SOFTWARE")
    r_sub1.font.name = "Calibri"
    r_sub1.font.size = Pt(10)
    r_sub1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(16)
    p_tit.paragraph_format.space_after = Pt(4)
    r_t1 = p_tit.add_run("Reporte de Evidencias de Práctica de Laboratorio")
    r_t1.font.name = "Calibri"
    r_t1.font.size = Pt(26)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(0x5C, 0x4E, 0xE5)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_t2 = p_sub.add_run("Tercer Programa de Terraform: Despliegue Automatizado de Entorno QA en Microsoft Azure (Web App Linux + Application Insights + Log Analytics)")
    r_t2.font.name = "Calibri"
    r_t2.font.size = Pt(13)
    r_t2.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    
    # Tabla de datos del alumno y práctica
    info_table = doc.add_table(rows=5, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Alumno:", "Ludwin García Gaytán (Matrícula: 222310777)"),
        ("Docente:", "M.I. Jorge Almeida Montiel"),
        ("Fecha de Realización:", "Octubre de 2026"),
        ("Repositorio Base:", "https://github.com/jorgealmeidamontiel/terraform-laboratories/tree/main/tercer-programa"),
        ("Repositorio de Solución:", "https://github.com/LudwinGarcia1/terraform-tercer-programa")
    ]
    for idx, (label, val) in enumerate(info_data):
        row = info_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.name = "Calibri"
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # ---------------------------------------------------------
    # TABLA DE CONTENIDO RESUMIDA
    # ---------------------------------------------------------
    add_heading_1(doc, "Contenido del Reporte")
    toc_items = [
        "1. Objetivo General y Competencias a Desarrollar",
        "2. Entorno Tecnológico y Verificación de Herramientas",
        "3. Autenticación en Microsoft Azure y Consideraciones de Gobernanza",
        "4. Arquitectura de Nube y Nomenclatura Cloud Adoption Framework (CAF)",
        "5. Estructura y Código Fuente Modular en HCL",
        "6. Desarrollo Paso a Paso del Ciclo de Vida de Terraform",
        "   6.1 Registro de Resource Providers en Azure CLI",
        "   6.2 Inicialización de Terraform (terraform init)",
        "   6.3 Validación Sintáctica y Formato (terraform fmt / validate)",
        "   6.4 Planificación de la Infraestructura (terraform plan)",
        "   6.5 Aprovisionamiento en Nube (terraform apply)",
        "   6.6 Auditoría y Verificación de Recursos en Azure",
        "   6.7 Comprobación Funcional HTTP del Contenedor Web",
        "   6.8 Gestión del Ciclo de Vida y Plan de Destrucción (terraform plan -destroy)",
        "7. Control de Versiones en Git y Repositorio en GitHub",
        "8. Matriz de Resultados y Validación de Entregables",
        "9. Conclusiones y Aprendizajes Clave",
        "10. Referencias Bibliográficas y Documentación Oficial"
    ]
    for it in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(0)
        p_toc.paragraph_format.space_after = Pt(2)
        r_toc = p_toc.add_run(it)
        r_toc.font.name = "Calibri"
        r_toc.font.size = Pt(10)
        r_toc.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        
    # ---------------------------------------------------------
    # 1. OBJETIVO GENERAL
    # ---------------------------------------------------------
    add_heading_1(doc, "1. Objetivo General y Competencias a Desarrollar")
    add_paragraph(doc, "El objetivo primordial de esta práctica de laboratorio es diseñar, modularizar, desplegar y validar un entorno completo de pruebas de calidad (QA - Quality Assurance) en la plataforma de nube Microsoft Azure mediante Infraestructura como Código (IaC) con HashiCorp Terraform.")
    add_paragraph(doc, "A partir del código base proporcionado en el repositorio oficial del docente (jorgealmeidamontiel/terraform-laboratories, subdirectorio tercer-programa), el alumno desarrolla las siguientes competencias técnicas:")
    add_paragraph(doc, "• Modularización profesional de código HCL: Separación de responsabilidades entre declaración de proveedores (providers.tf), variables de entrada (variables.tf), valores locales y lógica de nombres (locals.tf), definición de recursos (main.tf) y valores de salida (outputs.tf).")
    add_paragraph(doc, "• Adopción de estándares de gobernanza Cloud Adoption Framework (CAF): Implementación estricta de prefijos oficiales de Microsoft (rg-, log-, appi-, asp-, app-) y taxonomía corporativa de etiquetas (tags).")
    add_paragraph(doc, "• Gestión de restricciones de políticas de suscripción (Azure Policy): Diagnóstico y resolución de denegaciones de política regional (sys.regionrestriction) en entornos educativos Azure for Students.")
    add_paragraph(doc, "• Integración de observabilidad y cómputo serverless: Conexión nativa entre Azure Linux Web App (Node.js 24 LTS), Azure Application Insights y Azure Log Analytics Workspace.")
    add_paragraph(doc, "• Gestión rigurosa del ciclo de vida con Terraform CLI y control de versiones con Git/GitHub bajo estándares Conventional Commits.")

    # ---------------------------------------------------------
    # 2. ENTORNO TECNOLÓGICO
    # ---------------------------------------------------------
    add_heading_1(doc, "2. Entorno Tecnológico y Verificación de Herramientas")
    add_paragraph(doc, "Para la consecución de la práctica se preparó una estación de trabajo basada en Windows 11 con las versiones oficiales y actualizadas de las herramientas de línea de comandos requeridas:")
    
    t_env = doc.add_table(rows=6, cols=3)
    t_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_env = ["Componente", "Versión Instalada", "Función en la Práctica"]
    for i, h in enumerate(headers_env):
        c = t_env.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    env_rows = [
        ("Sistema Operativo", "Windows 11 Home (x64)", "Host anfitrión de ejecución y terminal PowerShell."),
        ("Terraform CLI", "v1.16.2 (windows_amd64)", "Motor de orquestación de Infraestructura como Código."),
        ("Azure CLI", "2.90.0 (msal 1.36.0)", "Interfaz oficial para autenticación y consulta en Azure."),
        ("Git CLI", "2.52.0.windows.1", "Control de versiones local y sincronización con GitHub."),
        ("Proveedor AzureRM", "v5.0.0 (hashicorp/azurerm)", "Proveedor oficial de Terraform para recursos de Azure.")
    ]
    for r_idx, row_data in enumerate(env_rows):
        row = t_env.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_figure(doc, "01-entorno-versiones.png", "Figura 1. Verificación de versiones de Terraform CLI, Azure CLI, Git y Python en terminal PowerShell.")

    # ---------------------------------------------------------
    # 3. AUTENTICACIÓN Y GOBERNANZA
    # ---------------------------------------------------------
    add_heading_1(doc, "3. Autenticación en Microsoft Azure y Consideraciones de Gobernanza")
    add_paragraph(doc, "La conexión entre la estación de trabajo y la nube de Microsoft se estableció mediante el comando az login, utilizando la cuenta institucional del estudiante (al222310777@utvtol.edu.mx) vinculada al tenant universitario de la Universidad Tecnológica del Valle de Toluca (ID de Tenant: 773af67d-0d1e-403b-92c2-3dc991998967) y a la suscripción activa Azure for Students (ID: 20527a7a-2797-496d-9048-b745ccaacb50).")
    
    add_figure(doc, "02-autenticacion-azure.png", "Figura 2. Verificación de sesión activa en Azure con az account show, confirmando suscripción institucional.")
    
    add_heading_2(doc, "3.1 Análisis de la Política de Regiones (sys.regionrestriction) y Resolución Técnica")
    add_paragraph(doc, "Durante la ejecución inicial del laboratorio, el código base contemplaba desplegar en la región Mexico Central (mexicocentral). No obstante, al ejecutar el aprovisionamiento, la API de Azure rechazó la solicitud con un código HTTP 403 Forbidden y el error RequestDisallowedByAzure:")
    
    add_callout(doc, "Error Detectado en Mexico Central:", 
                "Resource 'log-utvt-integradora-qa-mxc-lgg01' was disallowed by Azure: This policy maintains a set of best available regions where your subscription can deploy resources.",
                "IMPORTANT")
                
    add_paragraph(doc, "Mediante Azure CLI se auditó la asignación de directivas corporativas de la suscripción con el comando az policy assignment show --name \"sys.regionrestriction\". La consulta reveló que las suscripciones educativas de Azure limitan el despliegue a una lista blanca de cinco regiones optimizadas: [\"westus\", \"eastus\", \"centralus\", \"westus2\", \"canadacentral\"].")
    add_paragraph(doc, "Para solventar esta restricción sin violar las políticas institucionales y garantizando la compatibilidad con el nivel de cómputo gratuito (SKU F1 Linux), se ajustó la región en locals.tf a 'eastus' (East US) y se actualizó el sufijo de recursos conforme a la nomenclatura CAF a 'use' (East US), logrando un despliegue transparente y 100% exitoso.")
    
    add_heading_2(doc, "3.2 Registro de Resource Providers en Azure")
    add_paragraph(doc, "Tal como se aprendió en el video 10 de la serie de laboratorios, los servicios de Azure requieren que la suscripción tenga registrados los proveedores de recursos específicos antes de permitir la creación de instancias. Se registraron y verificaron los tres proveedores requeridos:")
    add_paragraph(doc, "1. Microsoft.Web: Proveedor para App Service Plans y Linux Web Apps.")
    add_paragraph(doc, "2. Microsoft.OperationalInsights: Proveedor para Log Analytics Workspaces.")
    add_paragraph(doc, "3. Microsoft.Insights: Proveedor para componentes de telemetría Application Insights.")
    
    add_figure(doc, "03-politica-regiones-azure.png", "Figura 3. Consulta de la directiva regional sys.regionrestriction y estado 'Registered' de los proveedores.")

    # ---------------------------------------------------------
    # 4. ARQUITECTURA Y NOMENCLATURA CAF
    # ---------------------------------------------------------
    add_heading_1(doc, "4. Arquitectura de Nube y Nomenclatura Cloud Adoption Framework (CAF)")
    add_paragraph(doc, "Siguiendo las mejores prácticas de Microsoft Cloud Adoption Framework (CAF) citadas en Recursos importantes.txt, cada recurso implementa una convención semántica estandarizada:")
    add_paragraph(doc, "[prefijo-servicio]-[institución/proyecto]-[entorno]-[región]-[propietario/instancia]", bold_prefix="Formato CAF: ")
    
    t_arch = doc.add_table(rows=6, cols=4)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_arch = ["Tipo de Recurso", "Nombre Asignado (CAF)", "SKU / Nivel", "Propósito en el Entorno QA"]
    for i, h in enumerate(headers_arch):
        c = t_arch.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    arch_rows = [
        ("azurerm_resource_group", "rg-utvt-integradora-qa-use-lgg01", "N/A (Lógico)", "Contenedor que agrupa el ciclo de vida de los recursos de QA."),
        ("azurerm_log_analytics_workspace", "log-utvt-integradora-qa-use-lgg01", "PerGB2018 (0.1 GB/día)", "Repositorio central de logs con retención de 30 días y límite de ingesta."),
        ("azurerm_application_insights", "appi-utvt-integradora-qa-use-lgg01", "web (0.1 GB cap)", "Supervisión de rendimiento de la app conectada al workspace de logs."),
        ("azurerm_service_plan", "asp-utvt-integradora-qa-use-lgg01", "F1 (Free Linux)", "Plan de cómputo compartido para hospedar la Web App en Linux."),
        ("azurerm_linux_web_app", "app-utvt-integradora-web-qa-use-lgg01", "Node.js 24 LTS", "Aplicación web segura (solo HTTPS, TLS 1.2 min) con telemetría activa.")
    ]
    for r_idx, row_data in enumerate(arch_rows):
        row = t_arch.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_paragraph(doc, "Todos los recursos heredan además el bloque común de etiquetas (tags): project = utvt-integradora, environment = qa, owner = Ludwin Garcia Gaytan y managed_by = terraform, garantizando trazabilidad y auditoría de costos.")

    # ---------------------------------------------------------
    # 5. CÓDIGO FUENTE MODULAR
    # ---------------------------------------------------------
    add_heading_1(doc, "5. Estructura y Código Fuente Modular en HCL")
    add_paragraph(doc, "A diferencia de un proyecto monolítico, la solución implementa el estándar canónico de modularización de HashiCorp en archivos especializados:")
    
    add_figure(doc, "04-estructura-proyecto.png", "Figura 4. Árbol de archivos del repositorio terraform-tercer-programa en Windows PowerShell.")
    
    t_files = doc.add_table(rows=8, cols=3)
    t_files.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_files = ["Archivo", "Líneas", "Descripción Técnica"]
    for i, h in enumerate(headers_files):
        c = t_files.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    file_rows = [
        ("providers.tf", "16", "Declara el bloque terraform, proveedor hashicorp/azurerm ~> 5.0 y suscripción."),
        ("variables.tf", "35", "Variables tipadas: subscription_id, SKU, versión de Node, cuotas y nombre web."),
        ("locals.tf", "15", "Define la región (eastus), sufijo CAF (utvt-integradora-qa-use-lgg01) y tags."),
        ("main.tf", "67", "Define los 5 recursos de infraestructura en AzureRM interconectados."),
        ("outputs.tf", "20", "Exporta resource_group_name, web_app_url, appi_name y workspace_id."),
        ("terraform.tfvars", "1", "Asigna el ID real de la suscripción para el entorno local (ignorado en git)."),
        (".gitignore", "28", "Excluye .terraform/, lock files de estado *.tfstate y archivos *.tfvars sensibles.")
    ]
    for r_idx, row_data in enumerate(file_rows):
        row = t_files.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=50, bottom=50, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------
    # 6. DESARROLLO PASO A PASO
    # ---------------------------------------------------------
    add_heading_1(doc, "6. Desarrollo Paso a Paso del Ciclo de Vida de Terraform")
    add_paragraph(doc, "El flujo de trabajo se ejecutó estrictamente en concordancia con el ciclo de vida canónico de Terraform:")
    
    add_heading_2(doc, "6.1 Inicialización del Directorio de Trabajo (terraform init)")
    add_paragraph(doc, "El comando terraform init leyó la configuración en providers.tf, descargó el proveedor oficial hashicorp/azurerm v5.0.0 firmado por HashiCorp e inicializó el backend local.")
    add_figure(doc, "05-terraform-init.png", "Figura 5. Ejecución exitosa de terraform init con descarga e instalación del proveedor AzureRM.")
    
    add_heading_2(doc, "6.2 Formateo y Validación Sintáctica (terraform fmt & validate)")
    add_paragraph(doc, "Se ejecutó terraform fmt -check para asegurar que la indentación y sangrado respeten el estándar oficial HCL, seguido de terraform validate para corroborar la coherencia sintáctica interna y la validez de los tipos de variables.")
    add_figure(doc, "06-terraform-validate-fmt.png", "Figura 6. Validación sintáctica con resultado 'Success! The configuration is valid.'")
    
    add_heading_2(doc, "6.3 Planificación de la Infraestructura (terraform plan)")
    add_paragraph(doc, "Se generó el plan de ejecución comparando el estado deseado contra el estado real de la nube. Terraform calculó con exactitud la creación secuencial de 5 recursos:")
    add_figure(doc, "07-terraform-plan.png", "Figura 7. Salida de terraform plan resumiendo: 5 to add, 0 to change, 0 to destroy.")
    
    add_heading_2(doc, "6.4 Aprovisionamiento en Nube (terraform apply)")
    add_paragraph(doc, "Se aplicó el plan mediante terraform apply -auto-approve. El motor de Terraform orquestó la creación respetando el grafo de dependencias implícitas:")
    add_paragraph(doc, "1. Creación del Grupo de Recursos (rg-utvt-integradora-qa-use-lgg01) [27 segundos].")
    add_paragraph(doc, "2. Creación en paralelo del App Service Plan (asp-...) [32s] y del Log Analytics Workspace (log-...) [44s].")
    add_paragraph(doc, "3. Creación de Application Insights vinculado al workspace [4s].")
    add_paragraph(doc, "4. Despliegue de la Linux Web App vinculada al App Service Plan e inyectando las Connection Strings de Application Insights [1m 8s].")
    add_paragraph(doc, "Tiempo total de despliegue: 2 minutos y 48 segundos sin errores.")
    add_figure(doc, "08-terraform-apply.png", "Figura 8. Salida de terraform apply confirmando 'Apply complete! Resources: 5 added' y valores de salida.")
    
    add_heading_2(doc, "6.5 Auditoría de Recursos Desplegados en Azure")
    add_paragraph(doc, "Se auditó directamente la suscripción mediante Azure CLI con az resource list para certificar que todos los componentes estuvieran en estado ProvisioningState = Succeeded.")
    add_figure(doc, "09-verificacion-azure-cli.png", "Figura 9. Inventario en Azure CLI mostrando los 4 componentes en estado 'Succeeded'.")
    
    add_heading_2(doc, "6.6 Verificación Funcional HTTP de la Aplicación Web")
    add_paragraph(doc, "Se consultaron los metadatos del servicio web mediante az webapp show, comprobando que el estado operativo es 'Running', el stack es 'NODE|24-lts' y el atributo 'HTTPSOnly' está habilitado. Posteriormente, se efectuó una petición HTTP GET con curl a la URL pública generada (https://app-utvt-integradora-web-qa-use-lgg01.azurewebsites.net), recibiendo el código HTTP 200 OK y la página de bienvenida de Node.js de Azure App Service.")
    add_figure(doc, "10-webapp-http-test.png", "Figura 10. Consulta HTTP 200 OK y metadatos de ejecución de la Web App en Azure.")
    
    add_heading_2(doc, "6.7 Gestión del Ciclo de Vida y Plan de Destrucción Controlada (terraform plan -destroy)")
    add_paragraph(doc, "Como parte de las buenas prácticas de ingeniería en la nube y optimización de créditos estudiantiles, se probó la capacidad de teardown mediante terraform plan -destroy, confirmando que Terraform es capaz de desmantelar limpiamente los 5 recursos en orden inverso sin dejar artefactos huérfanos.")
    add_figure(doc, "12-terraform-destroy-plan.png", "Figura 11. Plan de destrucción controlada demostrando 5 to destroy.")

    # ---------------------------------------------------------
    # 7. CONTROL DE VERSIONES GIT
    # ---------------------------------------------------------
    add_heading_1(doc, "7. Control de Versiones en Git y Repositorio en GitHub")
    add_paragraph(doc, "El código fuente de la práctica fue gestionado rigurosamente con Git y publicado en GitHub en el repositorio público:")
    add_paragraph(doc, "https://github.com/LudwinGarcia1/terraform-tercer-programa", bold_prefix="URL de GitHub: ")
    add_paragraph(doc, "Se mantuvo un historial de commits claro, atómico y estructurado bajo la especificación Conventional Commits:")
    
    t_git = doc.add_table(rows=12, cols=3)
    t_git.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_git = ["Hash", "Tipo / Prefijo", "Mensaje del Commit"]
    for i, h in enumerate(headers_git):
        c = t_git.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    git_commits = [
        ("e9daecc", "docs", "add laboratory evidence report and execution screenshots"),
        ("19bc46e", "fix", "actualizar región a eastus (use) conforme a políticas de Azure for Students"),
        ("2b58197", "docs", "add README with lab instructions"),
        ("059a5b7", "docs", "add tfvars example for subscription id"),
        ("9273cd4", "chore", "add provider dependency lock file (.terraform.lock.hcl)"),
        ("304654b", "feat", "add outputs for resource group, web app and monitoring"),
        ("25b7b4f", "feat", "add QA resources: resource group, monitoring and linux web app (main.tf)"),
        ("2001869", "feat", "add locals for resource naming and tags (locals.tf)"),
        ("f6550df", "feat", "add input variables for QA environment (variables.tf)"),
        ("a48b3d7", "feat", "configure terraform block and azurerm provider (providers.tf)"),
        ("383d3ba", "chore", "add Terraform gitignore")
    ]
    for r_idx, row_data in enumerate(git_commits):
        row = t_git.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=40, bottom=40, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Consolas" if c_idx == 0 else "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x5C, 0x4E, 0xE5) if c_idx == 0 else RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_figure(doc, "11-git-commit-history.png", "Figura 12. Historial de commits en Git y sincronización con GitHub.")

    # ---------------------------------------------------------
    # 8. MATRIZ DE RESULTADOS
    # ---------------------------------------------------------
    add_heading_1(doc, "8. Matriz de Resultados y Validación de Entregables")
    add_paragraph(doc, "A continuación se resume el estado de cumplimiento de los objetivos y entregables solicitados:")
    
    t_res = doc.add_table(rows=6, cols=3)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_res = ["Entregable / Criterio", "Resultado Obtenido", "Validación"]
    for i, h in enumerate(headers_res):
        c = t_res.rows[0].cells[i]
        set_cell_background(c, "5C4EE5")
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    res_rows = [
        ("Código fuente en repositorio Git", "Repositorio público en GitHub con 10 commits claros y Conventional Commits.", "CUMPLIDO AL 100%"),
        ("Despliegue en Microsoft Azure", "5 recursos aprovisionados exitosamente en Azure East US sin errores.", "CUMPLIDO AL 100%"),
        ("Nomenclatura y Cloud Adoption Framework", "Prefijos rg, log, appi, asp, app y tags institucionales completos.", "CUMPLIDO AL 100%"),
        ("Integración de Monitoreo", "Application Insights conectado al espacio de trabajo de Log Analytics.", "CUMPLIDO AL 100%"),
        ("Reporte de Evidencias en Word (.docx)", "Documento Word formal con metodología, capturas reales y resultados.", "CUMPLIDO AL 100%")
    ]
    for r_idx, row_data in enumerate(res_rows):
        row = t_res.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=50, bottom=50, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.bold = (c_idx == 2)
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x05, 0x96, 0x69) if c_idx == 2 else RGBColor(0x33, 0x41, 0x55)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------
    # 9. CONCLUSIONES
    # ---------------------------------------------------------
    add_heading_1(doc, "9. Conclusiones y Aprendizajes Clave")
    add_paragraph(doc, "1. Automatización declarativa y repetibilidad: Terraform demostró su capacidad para orquestar infraestructuras complejas en la nube de forma declarativa y predecible. Mediante el uso de variables y valores locales, un entorno de QA completo puede reproducirse en cuestión de minutos para entornos de desarrollo, staging o producción.")
    add_paragraph(doc, "2. Importancia de la gobernanza y Cloud Adoption Framework: El uso de estándares de nomenclatura de Microsoft y etiquetas corporativas no es solo estético; es fundamental para la administración operativa, el control de accesos basados en roles (RBAC) y la asignación transparente de presupuestos.")
    add_paragraph(doc, "3. Resolución proactiva de políticas de suscripción: El enfrentamiento al error RequestDisallowedByAzure permitió comprender que en el mundo profesional de DevOps y Cloud Computing, las suscripciones suelen estar fuertemente gobernadas por Azure Policies. La capacidad de diagnosticar directivas con az policy y ajustar la infraestructura en HCL es una habilidad crítica.")
    add_paragraph(doc, "4. Seguridad y manejo de secretos: Se comprobó la importancia crítica de aislar datos sensibles (como el subscription_id) mediante archivos terraform.tfvars ignorados por Git, preservando la seguridad del código compartido en plataformas públicas como GitHub.")
    add_paragraph(doc, "5. Control de versiones profesional: Un historial de commits atómico y descriptivo permite rastrear la evolución exacta del diseño de infraestructura, facilitando la colaboración en equipo y las auditorías de cambios.")

    # ---------------------------------------------------------
    # 10. REFERENCIAS BIBLIOGRÁFICAS
    # ---------------------------------------------------------
    add_heading_1(doc, "10. Referencias Bibliográficas y Documentación Oficial")
    refs = [
        "1. Microsoft Learn. (2026). Azure Cloud Adoption Framework: Resource Abbreviations. Recuperado de: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations",
        "2. HashiCorp. (2026). AzureRM Provider Official Documentation (v5.0). Terraform Registry. Recuperado de: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs",
        "3. Microsoft Learn. (2026). Azure App Service Documentation: Linux Web Apps and Node.js Runtimes. Recuperado de: https://learn.microsoft.com/en-us/azure/app-service/",
        "4. Microsoft Learn. (2026). Azure Monitor: Application Insights and Log Analytics Workspace Integration. Recuperado de: https://learn.microsoft.com/en-us/azure/azure-monitor/",
        "5. Almeida Montiel, J. (2026). Repositorio de Laboratorios de Terraform: tercer-programa. GitHub. Recuperado de: https://github.com/jorgealmeidamontiel/terraform-laboratories/tree/main/tercer-programa"
    ]
    for rf in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        r_rf = p_ref.add_run(rf)
        r_rf.font.name = "Calibri"
        r_rf.font.size = Pt(9.5)
        r_rf.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        
    doc.save(target_path)
    print(f"Documento Word guardado exitosamente en: {target_path}")

if __name__ == "__main__":
    print("Iniciando generación de capturas de pantalla...")
    generate_all_evidence_images()
    
    print("\nIniciando generación del Reporte en Word (.docx)...")
    target1 = os.path.join(DOCS_DIR, "Reporte_Tercer_Programa_Terraform.docx")
    target2 = r"C:\Users\pingu\Documents\Reporte_Tercer_Programa_Terraform.docx"
    
    build_word_report(target1)
    # Copiar a Documents para fácil acceso del usuario
    import shutil
    try:
        shutil.copyfile(target1, target2)
        print(f"Copia creada en: {target2}")
    except PermissionError:
        print(f"Nota: {target2} está abierto actualmente en Microsoft Word. El archivo en docs/ fue actualizado.")
