import React from 'react'
import axios from "axios";
import configData from "../../configFile.json";

export default class HeaderComponent extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            health: 0,
            isLoaded: false
        }
    }

    contextUpdate(context, delta){
        if(delta.includes('theme')){
            this.setState(()=>{
                return {theme:context.theme}
            })
        }
    }

    getHealth(){
        axios.get(location.protocol + configData.SERVER_URL + 'health').then (res => {
            this.setState({ health: res.data.health, isLoaded: true })});
    }
    componentDidMount(){
        this.getHealth()
        this.interval = setInterval(() =>
        this.getHealth(), 5000);
    }


    componentWillUnmount(){
        clearInterval(this.interval);
    }

    render(){
        if (this.state.isLoaded) {
            return (<div className="healthHeader">
                health: {this.state.health}
            </div>)
        }
        else
        {
            return (
                <div className="healthHeader">
                    Loading...
                </div>
            )
        }
    }
}