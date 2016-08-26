shinyServer(
  function(input, output) {

    output$pie_gender <- renderPlot({
        plot_gender( genders = input$gender, devices = input$device )
    })

    output$pie_device <- renderPlot({
        plot_device( genders = input$gender, devices = input$device )
    })

    output$rate_by_time <- renderPlot({
        plot_rate( genders = input$gender, devices = input$device, time = input$time )
    })

    output$count_by_time <- renderPlot({
        plot_count( genders = input$gender, devices = input$device, time = input$time )
    })
  }
)
