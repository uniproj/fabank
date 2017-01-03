$(document).ready(function(){
if($("#p_date").html().indexOf(".")!=-1){
var date=toJalili($("#p_date").html().substr($("#p_date").html().lastIndexOf(",")+2),
    $("#p_date").html().substr(0,$("#p_date").html().indexOf(".")),
    $("#p_date").html().substr($("#p_date").html().indexOf(".")+2,$("#p_date").html().indexOf(" ")-2));
$("#p_date").html("زمان انتشار : "+date);}
else{
var date=toJalili($("#p_date").html().substr($("#p_date").html().lastIndexOf(",")+2),
    $("#p_date").html().substr(0,$("#p_date").html().indexOf(" ")),
    $("#p_date").html().substr($("#p_date").html().indexOf(" ")+1,$("#p_date").html().lastIndexOf(" ")-6));
$("#p_date").html("زمان انتشار : "+date);
}
});

JalaliDate = {
    g_days_in_month: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    j_days_in_month: [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
};

JalaliDate.gregorianToJalali = function(g_y, g_m, g_d)
{
    g_y = parseInt(g_y);
    g_m = parseInt(g_m);
    g_d = parseInt(g_d);
    var gy = g_y-1600;
    var gm = g_m-1;
    var gd = g_d-1;

    var g_day_no = 365*gy+parseInt((gy+3) / 4)-parseInt((gy+99)/100)+parseInt((gy+399)/400);

    for (var i=0; i < gm; ++i)
    g_day_no += JalaliDate.g_days_in_month[i];
    if (gm>1 && ((gy%4==0 && gy%100!=0) || (gy%400==0)))
    /* leap and after Feb */
    ++g_day_no;
    g_day_no += gd;

    var j_day_no = g_day_no-79;

    var j_np = parseInt(j_day_no/ 12053);
    j_day_no %= 12053;

    var jy = 979+33*j_np+4*parseInt(j_day_no/1461);

    j_day_no %= 1461;

    if (j_day_no >= 366) {
        jy += parseInt((j_day_no-1)/ 365);
        j_day_no = (j_day_no-1)%365;
    }

    for (var i = 0; i < 11 && j_day_no >= JalaliDate.j_days_in_month[i]; ++i) {
        j_day_no -= JalaliDate.j_days_in_month[i];
    }
    var jm = i+1;
    var jd = j_day_no+1;
    var mah;
switch(jm){
        case 1:
                    mah="فروردین";
                    break;
        case 2:
                    mah="اردیبهشت";
                    break;
        case 3:
                    mah="خرداد";
                    break;
        case 4:
                    mah="تیر";
                    break;
        case 5:
                    mah="مرداد";
                    break;
        case 6:
                    mah="شهریور";
                    break;
        case 7:
                    mah="مهر";
                    break;
        case 8:
                    mah="آبان";
                    break;
        case 9:
                    mah="آذر";
                    break;
        case 10:
                    mah="دی";
                    break;
        case 11:
                    mah="بهمن";
                    break;
        case 12:
                    mah="اسفند";
                    break;
        
    }
    var str=jd+" "+mah+" "+jy;
    return str;
}

function toJalili(y,m,d){
    var m2;
    switch(m){
        case "Jan":
                    m2=1;
                    break;
        case "Feb":
                    m2=2;
                    break;
        case "Mar":
                    m2=3;
                    break;
        case "Apr":
                    m2=4;
                    break;
        case "May":
                    m2=5;
                    break;
        case "June":
                    m2=6;
                    break;
        case "July":
                    m2=7;
                    break;
        case "Aug":
                    m2=8;
                    break;
        case "Sept":
                    m2=9;
                    break;
        case "Oct":
                    m2=10;
                    break;
        case "Nov":
                    m2=11;
                    break;
        case "Dec":
                    m2=12;
                    break;
        
    }
    return JalaliDate.gregorianToJalali(y,m2,d);

}