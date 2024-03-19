import React from 'react'
import './Home.css'
import { Button, Upload,Table, message } from "antd";
import { UploadOutlined } from '@ant-design/icons';
import { doUploadCSV } from '../api/api';
import { useState } from "react";

function Home() {
  const [down_url, setDownUrl] = useState("");
  const [type_list, setTypeList] = useState([]);
  const [type_col_list, setTypeColList] = useState([]);
  const [csv_list, setCSVList] = useState(false);
  const [csv_col_list, setCSVColList] = useState(false);

  function titleCol(first_row){
    var type_columns=[]
    for (var key in first_row){
      type_columns.push({title:key, dataIndex:key,key:key})
    }
    return type_columns;
  } 

  function uploadImg(file) {
    const formData = new FormData();
    formData.append("file", file.file);
    doUploadCSV(formData).then((res) => {
      if (res.status === 200 && res.data.success === 1) {
        setTypeColList(titleCol(res.data.data.type[0]));
        setTypeList(res.data.data.type);
        setCSVColList(titleCol(res.data.data.content[0]));
        setCSVList(res.data.data.content);
        setDownUrl(res.data.data.file);
      }else{
        message.error(res.data.data);
      }
    });
  }

  return (
    <div>
      <div className='home-main'>
        <div className='home-main-content'>
          <section className='home-upload'>
            <span className='home-upload-title'>Upload Your CSV ... </span>
            <span className='home-upload-des'> must be in .csv format</span>
            <Upload name="avatar" customRequest={uploadImg} showUploadList={false} accept=".csv">
              <Button icon={<UploadOutlined />} type="primary" size='large'>
                Upload
                </Button>
            </Upload>
          </section>
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

export default Home