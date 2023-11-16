#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(plotly)
library(tidyverse)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Mi título"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
          p(tags$b("Opciones:"), "estas son las opciones para el UI. Por favor seleccione alguna de ellas"),
          icon("fas fa-paw"),
          width = 6,
          sliderInput("bins",
                      "Number of bins:",
                      min = 1,
                      max = 50,
                      value = 30),
          
          selectInput(
            inputId = "edimer",
            label = "Ejemplo:",
            choices = c("Azul", "Rojo")
          )
          
        ),
        
        

        # Show a plot of the generated distribution
        mainPanel(width = 6,
           plotOutput("edimer2")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$edimer2 <- renderPlot({
      iris  %>% 
        ggplot(aes(x = Sepal.Length)) +
        geom_histogram()
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
