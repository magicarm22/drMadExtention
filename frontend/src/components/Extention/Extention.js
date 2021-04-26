import React from 'react'

import './Extention.css'
import TabPane from "./Tab-pane";
import Tabs from "./Tabs";
import Statistic from "../Statistic/Statistic";

export default class App extends React.Component{
    constructor(props){
        super(props)
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
    
    render(){
        return (
            <div className="main_window background">
                <div className="extention">
                    <div className="container">
                        <Tabs>
                          <TabPane name="Статистика" key="1">
                            <Statistic />
                          </TabPane>
                          <TabPane name="Инвентарь" key="2">
                            Content of Tab Pane 2
                          </TabPane>
                          <TabPane name="Рейды" key="3">
                            Content of Tab Pane 3
                          </TabPane>
                        </Tabs>
                    </div>
                </div>
            </div>
        )
    }
}