import React from 'react'
import Authentication from '../Authentication/Authentication'
import CommandListContainer from './CommandListContainer/CommandListContainer'

import './App.css'
import Extention from "../Extention/Extention";
import axios from 'axios';
import configData from "../../configFile.json";

export default class App extends React.Component{



    constructor(props){
        super(props)
        this.Authentication = new Authentication()

        this.anchor = this.queryParamParse().anchor
        //if the extension is running on twitch or dev rig, set the shorthand here. otherwise, set to null. 
        this.twitch = window.Twitch ? window.Twitch.ext : null
        this.state={
            finishedLoading:false,
            theme:'light',
            showComponent: false
        }
        this.clickShowExtention = this.clickShowExtention.bind(this);
    }

    queryParamParse(){
        let query = window.location.search
        let obj = {}
        query.substring(1).split('&').map(v=>{
            let s = v.split('=')
            obj[s[0]] = decodeURIComponent(s[1])
        })

        return obj
    }

    contextUpdate(context, delta){
        if(delta.includes('theme')){
            this.setState(()=>{
                return {theme:context.theme}
            })
        }
    }

    componentDidMount(){
        if(this.twitch){
            this.twitch.onAuthorized((auth)=>{
                this.Authentication.setToken(auth.token, auth.userId)
                console.log(auth.token)
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + auth.token
                if(!this.state.finishedLoading){
                    this.setState(()=>{
                        return {finishedLoading:true}
                    })
                }
            })

            this.twitch.onContext((context,delta)=>{
                this.contextUpdate(context,delta)
            })

            this.twitch.configuration.onChanged(()=>{
                let config = this.twitch.configuration.broadcaster ? this.twitch.configuration.broadcaster.content : ''
                try{
                    config = JSON.parse(config)
                }catch(e){
                    config = ''
                }

                this.setState(()=>{
                    return{
                        commands:config
                    }
                })
            })
        }
    }

    componentWillUnmount(){
        if(this.twitch){
            this.twitch.unlisten('broadcast', ()=>console.log('successfully unlistened'))
        }
    }
    
    render(){
        if(this.state.finishedLoading){
            return (
                <div className="full_extention">
                    <div className="mini_button">
                        <button onClick={this.clickShowExtention} className="info_button">
                            <span style={{color: 'white'}}>Info</span>
                        </button>
                    </div>
                    {this.state.showComponent ?
                       <Extention/> :
                       null
                    }
                </div>
            )
        }else{
            return (null)
        }
    }

    clickShowExtention() {
        this.setState({
          showComponent: !this.showComponent,
        });
    }
}