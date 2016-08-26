shinyUI(fluidPage(
  titlePanel("Funnel Analysis"),
  
  sidebarLayout(
    sidebarPanel(
      checkboxGroupInput("gender", 
        label = h3("Gender"),
        choices = list("Male" = "Male", "Female" = "Female"),
        selected = c("Male", "Female")),

      checkboxGroupInput("device", 
        label = h3("Device Type"),
        choices = list("Mobile" = "Mobile", "Desktop" = "Desktop"),
        selected = c("Mobile", "Desktop")),
      
      radioButtons("time", 
        label = h3("Aggregate by"),
        choices = list("Day" = 1, "Week" = 2),
        selected = 1)
    ),
  
    mainPanel(
      fluidRow(column(6, plotOutput("pie_gender")),
               column(6, plotOutput("pie_device"))),
      fluidRow(column(12, plotOutput("rate_by_time"))),
      fluidRow(column(12, plotOutput("count_by_time")))
    )
  )
))
