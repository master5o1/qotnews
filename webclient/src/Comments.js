import React from 'react';
import { Link } from 'react-router-dom';
import { HashLink } from 'react-router-hash-link';
import { Helmet } from 'react-helmet';
import moment from 'moment';
import localForage from 'localforage';
import { sourceLink, infoLine, ToggleDot } from './utils.js';

class Article extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			story: false,
			error: false,
		};
	}
	
	componentDidMount() {
		const id = this.props.match.params.id;

		localForage.getItem(id)
			.then(
				(value) => {
					this.setState({ story: value });
				}
			);

		fetch('/api/' + id)
			.then(res => res.json())
			.then(
				(result) => {
					this.setState({ story: result.story }, () => {
						const hash = window.location.hash.substring(1);
						if (hash) {
							document.getElementById(hash).scrollIntoView();
						}
					});
					localForage.setItem(id, result.story);
				},
				(error) => {
					this.setState({ error: true });
				}
			);
	}

	displayComment(story, c, level) {
		return (
			<div className={level ? 'comment lined' : 'comment'}>
				<div className='info'>
					<p>
						{c.author === story.author ? '[OP]' : ''} {c.author || '[Deleted]'}
						&#8203; | <HashLink to={'#'+c.author+c.date} id={c.author+c.date}>{moment.unix(c.date).fromNow()}</HashLink>
					</p>
				</div>

				<div className='text' dangerouslySetInnerHTML={{ __html: c.text }} />

				{level < 5 ?
					c.comments.map(i => this.displayComment(story, i, level + 1))
				:
					<div className='info'><p>[replies snipped]</p></div>
				}
			</div>
		);
	}

	render() {
		const id = this.props.match.params.id;
		const story = this.state.story;
		const error = this.state.error;

		return (
			<div className='container'>
				{error && <p>Connection error?</p>}
				{story ?
					<div className='article'>
						<Helmet>
							<title>{story.title} - QotNews Comments</title>
						</Helmet>

						<h1>{story.title}</h1>

						<div className='info'>
							<Link to={'/' + story.id}>View article</Link>
						</div>

						{infoLine(story)}

						<div className='comments'>
							{story.comments.map(c => this.displayComment(story, c, 0))}
						</div>
					</div>
				:
					<p>loading...</p>
				}
				<ToggleDot id={id} article={true} />
			</div>
		);
	}
}

export default Article;
