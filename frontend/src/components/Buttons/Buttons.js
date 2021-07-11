import React from "react";
import axios from "axios";
import Grid from "@material-ui/core/Grid";

export default class Buttons extends React.Component {


    constructor(props) {
        super(props)
        this.state = {
          showInjection: false,
          showShop: false,
          showRaids: false,
          showStats: false,
          showPack: false,
          showTrade: false,
          showHelp: false,
          showButtons: true
        };
    }

    contextUpdate(context, delta) {
        if (delta.includes('theme')) {
            this.setState(() => {
                return {theme: context.theme}
            })
        }
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    render() {
        return (
            <div className="button_grid">
                 <Grid container spacing={5}>
                     <Grid item xs>
                         <button className="action_button"/>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button"/>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button"/>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button"/>
                     </Grid>
                  </Grid>
                <Grid container spacing={5}>
                     <Grid item xs>
                         <button className="action_button" onClick={() => this.showComponent("showInjection")}>Укол</button>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button" onClick={() => this.showComponent("showShop")}>Магазин</button>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button" onClick={() => this.showComponent("showRaids")}>Рейды</button>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button" onClick={() => this.showComponent("showStats")}>Статистика</button>
                     </Grid>
                  </Grid>
                <Grid container spacing={5}>
                     <Grid item xs>
                         <button className="action_button" onClick={() => this.showComponent("showPack")}>Инвентарь</button>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button" onClick={() => this.showComponent("showTrade")}>Обмен</button>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button"/>
                     </Grid>
                     <Grid item xs>
                         <button className="action_button" onClick={() => this.showComponent("showHelp")}>Помощь</button>
                     </Grid>
                  </Grid>
                </div>
        )
    }
    showComponent(componentName)
    {
        console.log(componentName)
        const stateCopy = {...this.state};
        Object.keys(stateCopy).forEach(key => stateCopy[key] = false);
        stateCopy[componentName] = true;
        this.setState(stateCopy);
        console.log(stateCopy)
        this.props.changeComponent(stateCopy);
    }
}