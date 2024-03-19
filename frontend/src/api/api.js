import request from "../utils/request";

export function doUploadCSV(csv_file){
    return request.post('/filter/filter/upload/',csv_file);
}

export function doDelCSV(id){
    return request.post('/filter/filter/delete/',{"id":id});
}

export function doListRecord(){
    return request.get('/filter/filter/list/');
}

export function doGetDetail(id){
    return request.get('/filter/filter/detail/?id='+id);
}
