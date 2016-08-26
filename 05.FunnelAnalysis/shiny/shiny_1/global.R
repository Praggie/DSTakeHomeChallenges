require(shiny)
require(ggplot2)
require(data.table)
require(reshape2)
dat <- fread("../../processing/joined_table.csv", sep=",", header=TRUE, na.strings="None")
dat$Date <- as.Date(dat$Date)
start_date <- min(dat$Date)

plot_gender <- function(genders, devices){
    use_dat <- dat[(dat$Sex %in% genders) & (dat$Device %in% devices),]
    pie <- ggplot(use_dat, aes(x=factor(1), fill=factor(Sex))) + 
        geom_bar(width = 1) + coord_polar(theta = "y") + theme_bw()
    print(pie)
}

plot_device <- function(genders, devices){
    use_dat <- dat[(dat$Sex %in% genders) & (dat$Device %in% devices),]
    pie <- ggplot(use_dat, aes(x=factor(1), fill=factor(Device))) + 
        geom_bar(width = 1) + coord_polar(theta = "y") + theme_bw()
    print(pie)
}

plot_count <- function(genders, devices, time){
    use_dat <- dat[(dat$Sex %in% genders) & (dat$Device %in% devices),]
    if(time == 1){
        use_dat$time <- use_dat$Date
    } else if(time == 2){
        use_dat$time <- floor((use_dat$Date - start_date) / 7)
    } else{
        use_dat$time <- format(use_dat$Date, "%m")
    }
    counted = use_dat[, .(home = sum(!is.na(HomePage)), 
                          search = sum(!is.na(SearchPage)),
                          payment = sum(!is.na(PaymentPage)),
                          paymentConfirm = sum(!is.na(ConfirmationPage))), by = c("time")]
    counted <- as.data.frame(counted)
    counted[,c("home", "search", "payment")] <- counted[,c("home", "search", "payment")] - counted[,c("search", "payment", "paymentConfirm")]
    counted_melt <- melt(counted, id="time")
    counted_melt$variable <- factor(counted_melt$variable, levels=c("paymentConfirm", "payment", "search", "home"))
    counted_melt <- counted_melt[order(counted_melt$variable),]
    p <- ggplot(counted_melt, aes(x=time, y=value, fill=variable)) + geom_area() + theme_bw()
    print(p)
}

plot_rate <- function(genders, devices, time){
    use_dat <- dat[(dat$Sex %in% genders) & (dat$Device %in% devices),]
    if(time == 1){
        use_dat$time <- use_dat$Date
    } else {
        use_dat$time <- floor((use_dat$Date - start_date) / 7)
    } 
    counted = use_dat[, .(home = sum(!is.na(HomePage)), 
                          search = sum(!is.na(SearchPage)),
                          payment = sum(!is.na(PaymentPage)),
                          paymentConfirm = sum(!is.na(ConfirmationPage))), by = c("time")]
    counted <- as.data.frame(counted)
    counted[,c("home", "search", "payment", "paymentConfirm")] <- counted[,c("home", "search", "payment", "paymentConfirm")] / counted[,c("home")]
    counted[,c("home", "search", "payment")] <- counted[,c("home", "search", "payment")] - counted[,c("search", "payment", "paymentConfirm")]
    counted_melt <- melt(counted, id="time")
    counted_melt$variable <- factor(counted_melt$variable, levels=c("paymentConfirm", "payment", "search", "home"))
    counted_melt <- counted_melt[order(counted_melt$variable),]
    p <- ggplot(counted_melt, aes(x=time, y=value, fill=variable)) + geom_area() + theme_bw()
    print(p)
}
