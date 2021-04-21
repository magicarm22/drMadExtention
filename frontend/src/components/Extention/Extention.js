import React from 'react'
import Authentication from '../Authentication/Authentication'

import './Extention.css'

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
        }
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
                <div className="main_window background">
                    <div className="extention">
                        <h2>Hello, World!</h2>
                        <p>Would you care to cycle a color?</p>
                        <div>
                            <input type="button" id="cycle" disabled="disabled" value="Yes, I would" />
                        </div>
                        <div style={{float: 'left', position: 'relative', left: '50%'}}>
                            <div id="color" style={{borderRadius: '50px', transition: 'background-color 0.5s ease', marginTop: '30px', width: '100px', height: '100px', backgroundColor: '#6441A4', float: 'left', position: 'relative', left: "-50%"}}>
                            </div>
                        </div>
                    </div>
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