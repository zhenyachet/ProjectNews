import React, {useState, useEffect} from 'react'
import axios from 'axios'

function DataFetching(){
	const [posts, setPosts] = useState([])

	useEffect(() => {
		axios.get('http://127.0.0.1:8000/twitter/get_list/')
			.then(res => {
				console.log(res)
				setPosts(res.data)
			})
			.catch(err => {
				console.log(err)
			})
	}, [])

    return (
        <div>
        	<ul>
        		{posts.map(post => (
        			<p key={post.twitter_id}>Twitter_user: {post.twitter_user}</p>
        		))}
        	</ul>
        </div>
    		)

}

export default DataFetching