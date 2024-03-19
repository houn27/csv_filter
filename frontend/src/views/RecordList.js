import React, { useState, useEffect } from 'react'
import './RecordList.css'
import { Card,message,Button } from 'antd';
import { doListRecord,doDelCSV } from '../api/api';
import exchange from '../utils/time';

function RecordList() {
  const [csv_list, setCSVList] = useState([]);

  useEffect(() => {
    doListRecord().then((res) => {
      if (res.status === 200 && res.data.success === 1) {
        setCSVList(res.data.data)
      }else{
        message.error(res.data.data);
      }
    })
  }, [])

  function delCSV(id){
    doDelCSV(id).then((res) => {
      if (res.status === 200 && res.data.success === 1) {
        setCSVList(res.data.data)
      }else{
        message.error(res.data.data);
      }
    })
  }

  return (
    <div>
      <div className='list-main'>
        <div className='list-main-content'>
          {csv_list.map((csv) => (
            <Card type="inner" title={csv.name} className='list-item' extra={<div><Button onClick={(e) =>delCSV(csv.id)} type="text" size='small'>Delete</Button> <a href={'/csv/'+csv.id}>More</a></div>}>
              <div className='list-item-content'>
                <span>Result:&nbsp; {csv.path}</span>
                <span className='list-item-date'>
                  {exchange(csv.create_date)}
                  
                </span>
              </div>
              
            </Card>
          ))}
          
        </div>
      </div>

    </div>
  )
}

export default RecordList
