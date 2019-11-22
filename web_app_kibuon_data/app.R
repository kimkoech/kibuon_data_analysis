#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

# packages
library(shiny)
library(readxl) # package for importing data
library("janitor")
library(ggplot2)
library(tidyverse)
library(markdown)




# Define UI for application that draws a 
ui <- navbarPage( "Kibuon Data Analysis",
                tabPanel("About",
                    includeMarkdown("About.Rmd"),
                    imageOutput("image_0")
                )
                ,
                navbarMenu("Visualization",
                           tabPanel("Survey Responses Map", 
                                    includeMarkdown("survey_responses_map.Rmd"),
                                    imageOutput("image_5")
                                    
                           ),
                           tabPanel("Map", includeMarkdown("map.Rmd"),
                                    imageOutput("image_1")
                           ),
                           
                           tabPanel("Population Distribution", 
                                    h1("Distribution of population per household")
                                    ,
                                    "Move the slider to change the bin size
                                    for the number of people in each house",
                                    HTML("<br>"),
          
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
                            ),
                           tabPanel("Age distribution", includeMarkdown("age_distribution.Rmd"),
                                    plotOutput("age_distribution")
                           ),
                           tabPanel("Distance distribution", "Paragraph description goes here",
                                    imageOutput("image_2")
                           ),
                           tabPanel("Water Usage", "Paragraph description goes here",
                                    plotOutput("plot_3"),
                                    plotOutput("plot_4")
                           )
                           
                           
                          ),
                
                tabPanel("Tour", "Hello")
)

# Define server logic required to draw a 
server <- function(input, output) {

   
    # load data
    file_path <- "../raw-data/survey_data.xlsx"
    survey_data <- read_xlsx(file_path, 
                             range = cell_rows(1:41)) %>%
        clean_names()
    
    # Distribution of number of people per household in the community
    output$distPlot <- renderPlot({
        # generate bins based on input$bins from ui.R
        y   <- survey_data$total
        bins <- seq(min(y), max(y), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
         hist(y, breaks = bins, col = 'darkgray', border = 'white',
              main = "Histogram of the distribution of total number of people per household",
              xlab = "Number of people per household",
              ylab = "Count")
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
     
     
     output$image_0 <- renderImage({ 
         about_page_map<- list(src = "map_plot.png", width = 600, height = 600, style="text-align: center;")
         about_page_map
     }, deleteFile = FALSE)
     
     output$image_1 <- renderImage({ 
         spatial_dist <- list(src = "spatial_dist.png", width = 600, height = 600, style="text-align: center;")
         spatial_dist
     }, deleteFile = FALSE)
     output$image_2 <- renderImage({ 
         spatial_dist <- list(src = "distance_dist_plots.png", width = 600, height = 600, style="text-align: center;")
         spatial_dist
     }, deleteFile = FALSE)
     
     output$plot_3 <-renderPlot({
         ggplot(survey_data, aes(y = household_liters_day, x= total))+
             geom_jitter(height = 0.2) + 
             geom_smooth(method = "glm", se= TRUE) +
             labs(
                 x = "Total number of people per household ",
                 title = "Linear model of water usage per day as a funcion of number of people",
                 subtitle = "Water usage is based on interview responses",
                 y = "Water usage per day in liters"
             )
     })
     
     output$plot_4 <-renderPlot({
         extrapolation <- read.csv("extrapolation.csv")
         ggplot(extrapolation, aes(y = estimate, x= number_of_people)) + geom_point() + geom_line() +
             labs(
                 x = "Total number of people per household ",
                 title = "Application of a linear model to estimate water usage",
                 subtitle = "Water usage is based on interview responses",
                 y = "Extrapolated water usage per day in liters"
             )
     })
     
     output$image_5 <- renderImage({ 
         survey_source <- list(src = "survey_source_map.png", width = 600, height = 600, style="text-align: center;")
         survey_source
     }, deleteFile = FALSE)
}

# Run the application 
shinyApp(ui = ui, server = server)
