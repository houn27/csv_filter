import { RouteObject } from 'react-router-dom'
import Home from '../views/Home'
import CSVDetail from '../views/CSVDetail'
import RecordList from '../views/RecordList'

const router: RouteObject[]=[
    {
        path:"/csv/:id",
        element:<CSVDetail />
    }, 
    {
        path:"/list",
        element:<RecordList />
    },
    {
        path:"/",
        element:<Home/>
    },
]

export default router