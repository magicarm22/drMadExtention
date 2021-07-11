import React from "react";


export default class InRaid extends React.Component {


    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false,
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
        if (this.state.isLoaded) {
            return (
                <div className="inRaid">

                </div>
            )
        }
        else {
            return ("Loading...")
        }
    }
}