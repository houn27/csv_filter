function exchange(dateTimeStamp){
      let result = '';
      
      //get number of second for minute, hour, day ...
      const minute = 60; 
      const hour = minute * 60;
      const day = hour * 24;
      const week = day * 7;
      
      //get time difference
      const diffValue = Math.floor(Date.now()/1000) - dateTimeStamp;
      //console.log(Math.floor(Date.now()/1000),dateTimeStamp)
   
      if (diffValue < 0) return;
      
      //get values of minute, hour, day ... for time difference
      const minC = diffValue / minute; 
      const hourC = diffValue / hour;
      const dayC = diffValue / day;
      const weekC = diffValue / week;
   
      if (weekC >= 1 && weekC <= 4) {
        weekC===1? result ='1 week ago' : result = ` ${Math.floor(weekC)} weeks ago`;
      } else if (dayC >= 1 && dayC <= 6) {
        dayC===1? result='1 day ago' : result = ` ${Math.floor(dayC)} days ago`;
      } else if (hourC >= 1 && hourC <= 23) {
        hourC===1? result='1 hour ago' : result = ` ${Math.floor(hourC)} hours ago`;
      } else if (minC >= 1 && minC <= 59) {
        minC===1? result='1 minute ago' : result = ` ${Math.floor(minC)} minutes ago`;
      } else if (diffValue >= 0 && diffValue <= minute) {
        result = 'just now';
      } else {
        const datetime = new Date();
        datetime.setTime(dateTimeStamp*1000);
        const Nyear = datetime.getFullYear();
        const Nmonth = datetime.getMonth() + 1 < 10 ? `0${datetime.getMonth() + 1}` : datetime.getMonth() + 1;
        const Ndate = datetime.getDate() < 10 ? `0${datetime.getDate()}` : datetime.getDate();
        result = `${Nyear}-${Nmonth}-${Ndate}`;
      }
   
      return result;
  
}

export default exchange;