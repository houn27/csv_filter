import React, { useState, useEffect }  from 'react'
import './CSVDetail.css'
import { Button, Table, message } from "antd";
import { doGetDetail } from '../api/api';
import { useParams} from "react-router-dom";

function CSVDetail() {
  const params = useParams();
  const [down_url, setDownUrl] = useState("");
  const [type_list, setTypeList] = useState([]);
  const [type_col_list, setTypeColList] = useState([]);
  const [csv_list, setCSVList] = useState(false);
  const [csv_col_list, setCSVColList] = useState(false);

  useEffect(() => {
    if (params.id !== undefined) {
      doGetDetail(params.id).then((res) => {
        if (res.status === 200 && res.data.success === 1) {
          setTypeColList(titleCol(res.data.data.type[0]));
          setTypeList(res.data.data.type);
          setCSVColList(titleCol(res.data.data.content[0]));
          setCSVList(res.data.data.content);
          setDownUrl(res.data.data.file);
        }else{
          message.error(res.data.data);
        }
      })
    }
  },[])

  function titleCol(first_row){
    var type_columns=[]
    for (var key in first_row){
      type_columns.push({title:key, dataIndex:key,key:key})
    }
    return type_columns;
  } 


  return (
    <div>
      <div className='detail-main'>
          <div className='detail-main-content'>
          <section className='home-types'>
              <span className='home-types-title'>Types</span>
              <Table className='home-types-table' scroll={{ x: 1000 }} columns={type_col_list} dataSource={type_list} />
          </section>
          <section className='home-types'>
              <span className='home-types-title'>Data</span>
            <Table className='home-types-table' scroll={{ x: 1000 }} columns={csv_col_list} dataSource={csv_list} />
          </section>
          <section className='home-types'>
            <Button type="link" size='large' href={down_url}>Download</Button>
          </section>
          </div>
        </div>
      </div>
  )
}

export default CSVDetail