import React from 'react';
import './App.css';
import DataFetching from './components/DataFetching';
//import { makeStyles } from '@material-ui/core';

/*const useStyles = makeStyles({
    appMain: {
        paddingLeft: '220px',
        width: '100%'
    }
    })*/

class App extends React.Component {
    render(){
        return(
        <>
            <DataFetching />
        </>
        )
    }
}

export default App;
