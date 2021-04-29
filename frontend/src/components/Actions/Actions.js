import React from 'react'
import axios from "axios";
import configData from "../../configFile.json";

export default class Actions extends React.Component{
    constructor(props){
        super(props)
        this.injection = this.injection.bind(this)
        this.state = {
          minutes: 0,
          error: null
        };
    }

    contextUpdate(context, delta){
        if(delta.includes('theme')){
            this.setState(()=>{
                return {theme:context.theme}
            })
        }
    }

    componentDidMount(){
    }


    componentWillUnmount(){
    }

    injection()
    {
        axios.post(location.protocol + configData.SERVER_URL + 'injection').then (res => {
            this.setState({ minutes: res.data.minutes})
        }
        );
    }


    render(){
        return (
            <div className="Actions">
                <button onClick={this.injection} className="injectionButton" />
                Вы на уколах еще: {this.state.minutes}
            </div>
        )
    }
}