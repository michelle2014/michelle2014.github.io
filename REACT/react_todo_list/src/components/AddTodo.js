import React, { Component } from 'react'
import PropTypes from 'prop-types';

export class AddTodo extends Component {

    state = {
        title: ''
    }

    onChange = (e) => this.setState({ title: e.target.value });

    onSubmit = (e) => {
        e.preventDefault()
        this.props.addTodo(this.state.title)
        this.setState({ title: '' })
    }

    render() {
        return (
            <form onSubmit={this.onSubmit} style={{ display: 'flex' }}>
                <input style={{ flex: '10' }}
                    type="text"
                    name="title"
                    placeholder="Add Todo..."
                    value={this.state.title}
                    onChange={this.onChange}
                />
                <input style={{ flex: '1' }}
                    type="submit"
                    value="Submit"
                    className="btn" 
                />
            </form>
        )
    }
}

AddTodo.propTypes = {
    addTodo: PropTypes.func.isRequired
}

export default AddTodo
