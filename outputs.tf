output "resource_group_name" {
  description = "Nombre del grupo de recursos"
  value       = azurerm_resource_group.qa.name
}

output "web_app_url" {
  description = "URL pública de la aplicación web"
  value       = "https://${azurerm_linux_web_app.qa.default_hostname}"
}

output "application_insights_name" {
  description = "Nombre del recurso de Application Insights"
  value       = azurerm_application_insights.qa.name
}

output "log_analytics_workspace_id" {
  description = "ID del espacio de trabajo de Log Analytics"
  value       = azurerm_log_analytics_workspace.qa.id
}
