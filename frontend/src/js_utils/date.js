import dayjs from "dayjs"

function parseDate(time, format, use_diff = false){

    time = dayjs(time);
    let now = dayjs();
    
    if (use_diff){
        if (now.diff(time, "minute") == 0){
            time = "방금 전"
        } else if (now.diff(time, "minute") < 60){
            time = `${now.diff(time, "minute")} 분 전`
        } else if (now.diff(time, "hour") < 7){
            time = `${now.diff(time, "hour")} 시간 전`
        } else {
            time = time.format(format) 
        }
        return time
    } else {
        return time.format(format) 
    }
};






export default parseDate;