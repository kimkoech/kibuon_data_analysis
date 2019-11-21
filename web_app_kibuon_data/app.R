#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(readxl) # package for importing data
library("janitor")
library(ggplot2)
library(tidyverse)


# load data
file_path <- "../raw-data/survey_data.xlsx"
survey_data <- read_xlsx(file_path, 
                         range = cell_rows(1:41)) %>%
    clean_names()

# Define UI for application that draws a histogram
ui <- navbarPage( "Kibuon Data Analysis",
                    tabPanel("About",
                             
                           # Sidebar with a slider input for number of bins 
                           sidebarLayout(
                                sidebarPanel(
                                    sliderInput("bins",
                                                "Number of bins:",
                                                min = 1,
                                                max = 40,
                                                value = 30)
                                ),
                                # Show a plot of the generated distribution
                                mainPanel(
                                   plotOutput("distPlot")
                                )
                        )
                )
                ,
                navbarMenu("Visualization",
                           tabPanel("Map", "Paragraph description goes here",
                                    imageOutput("image_1")
                           ),
                           tabPanel("Age distribution", "Paragraph description goes here",
                                    plotOutput("age_distribution")
                                    #imageOutput("image_1")
                           ))
                ,
                tabPanel("Tour", "Hello")
                
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    # Distribution of number of people per household in the community
    output$distPlot <- renderPlot({
        # generate bins based on input$bins from ui.R
        y   <- survey_data$total
        bins <- seq(min(y), max(y), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
         hist(y, breaks = bins, col = 'darkgray', border = 'white')
        #ggplot(survey_data, aes(x = total, bins = input$bins)) + geom_bar()
    })
    
     
   # Distribution of ages
     output$age_distribution <-renderPlot({
     ggplot(read.csv("gathered_ages.csv"), aes(x = age_range,
                               y = number_of_people,
                               group = age_range)) +
         geom_col(fill = "#6ef0d1") +
         labs(
             x = "Age range",
             title = "Distribution of ages in the community",
             subtitle = "Which age group has the largest population?",
             y = "Number of people"
         )
        })
     
     spatial_dist <- list(src = "spatial_dist.png", width = 600, height = 600, style="text-align: center;")
     
     output$image_1 <- renderImage({ 
         spatial_dist
     }, deleteFile = FALSE)
}

# Run the application 
shinyApp(ui = ui, server = server)
