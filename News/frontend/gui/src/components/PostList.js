import React, { Component } from 'react'
import axios from 'axios'


class PostList extends Component {
	constructor(props){
		super(props)

		this.state = {
			posts: []
		}
	}

	componentDidMount(){
		axios.get('http://127.0.0.1:8000/twitter/get_list/')
			.then(response => {
				console.log(response)
				this.setState({posts: response.data})
			})
			.catch(error =>{
				console.log(error)
			})
	}

    render(){
    	const { posts } = this.state
        return(
        <div>
        	List of posts
        	{
        	posts.length ?
        	posts.map(post => <div key={post.twitter_id}>{post.twitter_user}</div>):
        		null
        	}
        </div>
        )
    }
}

export default PostList;
