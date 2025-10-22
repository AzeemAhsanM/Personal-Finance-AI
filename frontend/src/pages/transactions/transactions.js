import React, { useState, useEffect } from 'react';
import api from '../../api';
import './transactions.css';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await api.get('/transactions/list');
        setTransactions(response.data);
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    };
    fetchTransactions();
  }, []);

  return (
    <div className="transactions-container">
      <h2>All Transactions</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx) => (
            <tr key={tx.id}>
              <td className="date"><span>{tx.date}</span></td>
              <td className="category"><span>{tx.category}</span></td>
              <td className={`amount ${tx.type === 'income' ? 'income-amount' : 'expense-amount'}`}>
                <span>{tx.type === 'income' ? '+' : '-'}₹{tx.amount.toFixed(2)}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>  
  );
};

export default Transactions;
