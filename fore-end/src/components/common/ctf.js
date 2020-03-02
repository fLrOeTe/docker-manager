import axios from 'axios'
import { longStackSupport } from 'q';
var ctf={
    list(){
        var that=this;
        axios.request({
        url: localStorage.getItem('address')+'api/CtfCompetitionTables/',
        method: 'GET',
        responseType: 'json'
        }).then(function(response) {
            return response.data
        }).catch(function (error) {
            return response.data
        }
        )
    }
}

export default ctf;