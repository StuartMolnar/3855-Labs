import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://lab6.eastus.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Book Withdrawal</th>
							<th>Book Return</th>
						</tr>
						<tr>
							<td># BW: {stats['num_bk_withdrawals']}</td>
							<td># BR: {stats['num_bk_returns']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Overdue Length: {stats['max_overdue_length']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Overdue Fine: {stats['max_overdue_fine']}</td>
						</tr>
						<tr>
							<td colspan="2">Longest Book Withdrawn: {stats['longest_book_withdrawn']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
