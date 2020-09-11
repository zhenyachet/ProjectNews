import React from 'react'
import {makeStyles} from '@material-ui/core';

const useStyles = makeStyles({
    sideMenu:{
        display:'flex',
        flexDirection: 'column',
        position: 'absolute',
        left: '0px',
        width: '220px',
        height: '100%',
        backgroundColor: 'blue'
    }
})

export default function SideMenu(){

    const classes = useStyles()
    console.log(classes)

    return (
        <div className={classes.sideMenu}>
        </div>
    )

}