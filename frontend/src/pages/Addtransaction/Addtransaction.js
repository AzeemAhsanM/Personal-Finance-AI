import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api';
import './Addtransaction.css';

const AddTransaction = () => {
  // State for the form fields
  const [type, setType] = useState('income'); // 'income' or 'expense'
  const [amount, setAmount] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]); // Default to today
  const [category, setCategory] = useState('');

  // State for UI feedback
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const navigate = useNavigate();

  // Define categories based on transaction type
  const expenseCategories = ['Food', 'Transportation', 'Housing', 'Bills', 'Entertainment', 'Travel', 'Other'];
  const incomeCategories = ['Salary', 'Freelance', 'Investment', 'Gift', 'Other'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess('');

    // Basic validation
    if (!amount || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount.');
      setIsLoading(false);
      return;
    }
    if (!category) {
        setError('Please select a category.');
        setIsLoading(false);
        return;
    }

    const transactionData = {
      amount: parseFloat(amount),
      type,
      category,
      date,
    };

    try {
      await api.post('/transactions/', transactionData); // Endpoint from your transactions_router.py
      setSuccess('Transaction added successfully!');
      
      // Clear the form
      setAmount('');
      setCategory('');

      // Redirect to the dashboard after a short delay to see the message
      setTimeout(() => navigate('/add'), 1500);

    } catch (err) {
      setError('Failed to add transaction. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="add-transaction-container">
      <form onSubmit={handleSubmit} className="transaction-form">
        <h2>New Transaction</h2>

        <div className="type-selector">
          <button
            type="button"
            className={`type-btn income-btn ${type === 'income' ? 'active' : ''}`}
            onClick={() => { setType('income'); setCategory(''); }}
          >
            Income
          </button>
          <button
            type="button"
            className={`type-btn expense-btn ${type === 'expense' ? 'active' : ''}`}
            onClick={() => { setType('expense'); setCategory(''); }}
          >
            Expense
          </button>
        </div>

        <div className="form-row">
            <div className="form-group">
                <label htmlFor="amount">Amount</label>
                <input
                    id="amount"
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="0.00"
                    step="0.01"
                />
            </div>
            <div className="form-group">
                <label htmlFor="date">Date</label>
                <input
                    id="date"
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
            </div>
        </div>

        <div className="form-group">
          <label htmlFor="category">Category</label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="" disabled>Select a category</option>
            {(type === 'income' ? incomeCategories : expenseCategories).map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        
        {error && <p className="form-error">{error}</p>}
        {success && <p className="form-success">{success}</p>}

        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? 'Adding...' : 'Add Transaction'}
        </button>
      </form>
    </div>
  );
};

export default AddTransaction;