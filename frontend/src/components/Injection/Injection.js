import React from 'react'
import axios from "axios";
import configData from "../../configFile.json";

export default class Injection extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            isLoaded: false,
            minutes: 0
        };
        this.injection()
    }

    contextUpdate(context, delta){
        if(delta.includes('theme')){
            this.setState(()=>{
                return {theme:context.theme}
            })
        }
    }

    componentDidMount(){
        this.interval = setInterval(() =>
        this.getMinutes(), 10000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    injection()
    {
        axios.post(location.protocol + configData.SERVER_URL + 'injection').then (res => {
            this.setState({ minutes: res.data.minutes})
            }
        );
    }

    getMinutes()
    {
        axios.get(location.protocol + configData.SERVER_URL + 'injection').then (res => {
            this.setState({ minutes: res.data.minutes})
            }
        );
    }


    render(){
        return (
            <div className="inInjection">
                Вы пришли на уколы. Вам осталось отдыхать {this.state.minutes} минут
            </div>
        )
    }
}