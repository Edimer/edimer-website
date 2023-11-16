
library(shiny)
library(shinythemes)

ui <- fluidPage(
  
  theme = shinytheme("cosmo"),
  
  navbarPage(
    "UNAL Medellín",
    tabPanel(
      "Paysandú",
      plotOutput("grafico1")
    ),
    tabPanel(
      "Cotové",
      fluidRow(
        column(
          width = 12,
          tableOutput("tabla1")
        )
      )
    ),
    navbarMenu(
      "San Pablo",
      tabPanel(
        "Porcicultura",
        plotOutput("grafico2")
      ),
      tabPanel(
        "Avicultura"
      )
    )
  )
  
)

server <- function(input, output) {
  
  output$grafico1 <- renderPlot({
    plot(iris)
  })
  
  output$tabla1 <- renderTable({
    iris
  })
  
  
  output$grafico2 <- renderPlot({
    plot(mtcars)
  })
  
}


shinyApp(ui = ui, server = server)
