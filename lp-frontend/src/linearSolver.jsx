import React, { useState, useEffect } from 'react';
import './linearSolver.css';

// New component for rendering tableaus
const TableauRenderer = ({ tableau, step }) => {
  if (!tableau || !tableau.length) return null;
  
  return (
    <div className="tableau-container">
      <div className="tableau-step">
        <span className="step-label">Step:</span> {step}
      </div>
      <div className="tableau-wrapper">
        <table className="tableau-table">
          <tbody>
            {tableau.map((row, rowIdx) => (
              <tr key={`row-${rowIdx}`}>
                {row.map((cell, cellIdx) => (
                  <td key={`cell-${rowIdx}-${cellIdx}`}>
                    {typeof cell === 'number' ? cell.toFixed(2) : cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Updated renderResults function to properly display solution, message, and tableaus
const renderResults = (data, onBack) => {
  const { solution, steps, cache, message } = data;

  return (
    <div className="lp-solver-card results-card">
      <h2>Linear Programming Solution</h2>

      {/* Solution Status Message */}
      <div className="solution-summary">
        <h3>Solution Status:</h3>
        <div className="solution-message">{message}</div>
      </div>

      {/* Solution Variables Table */}
      {solution && solution.length === 1 && solution[0].length === 2 && (
        <div className="solution-variables">
          <h3>Variable Values:</h3>
          <table className="variables-table">
            <thead>
              <tr>
                {solution[0][0].map((varName, idx) => (
                  <th key={`var-${idx}`}>{varName}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                {solution[0][1].map((value, idx) => (
                  <td key={`val-${idx}`}>
                    {typeof value === 'number' ? value.toFixed(4) : value}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* Tableaus */}
      {cache && cache.length > 0 && (
        <div className="tableaus-container">
          <h3>Tableaux Steps:</h3>
          <div className="tableaus-list">
            {cache.map((tableau, idx) => (
              <TableauRenderer
                key={`tableau-${idx}`}
                tableau={tableau}
                step={steps[idx] || `Step ${idx + 1}`}
              />
            ))}
          </div>
        </div>
      )}

      <div className="btn-container">
        <button onClick={onBack} className="btn btn-secondary">
          Back to Input
        </button>
      </div>
    </div>
  );
};

// Updated LinearProgrammingSolver component
const LinearProgrammingSolver = () => {
  // States for problem setup
  const [method, setMethod] = useState('simplex');
  const [numVariables, setNumVariables] = useState(2);
  const [numConstraints, setNumConstraints] = useState(2);
  const [numGoals, setNumGoals] = useState(1);
  const [step, setStep] = useState('setup');
  const [constraints, setConstraints] = useState([]);
  const [objectiveFunctions, setObjectiveFunctions] = useState([]);
  const [goalConstraints, setGoalConstraints] = useState([]);
  const [isMaximize, setIsMaximize] = useState(true);
  const [allNonNegative, setAllNonNegative] = useState(true);
  
  // States for solution
  const [solutionData, setSolutionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Initialize matrices when dimensions are set
  const initializeMatrices = () => {
    // Initialize constraints matrix
    const newConstraints = Array(numConstraints).fill().map(() => ({
      coefficients: Array(numVariables).fill(0),
      operator: '<=',
      rhs: 0
    }));
    setConstraints(newConstraints);
    
    if (method === 'goalProgramming') {
      // Initialize goal constraints for goal programming
      const newGoalConstraints = Array(numGoals).fill().map(() => ({
        coefficients: Array(numVariables).fill(0),
        operator: '=',
        rhs: 0,
        priority: 1
      }));
      setGoalConstraints(newGoalConstraints);
      
      // For goal programming, we don't use regular objective functions
      setObjectiveFunctions([]);
    } else {
      // Initialize standard objective function
      setObjectiveFunctions([{
        coefficients: Array(numVariables).fill(0)
      }]);
      
      // Clear goal constraints if not in goal programming mode
      setGoalConstraints([]);
    }
    
    setStep('input');
  };
  
  // Handle constraint coefficient change
  const handleConstraintChange = (constraintIdx, varIdx, value) => {
    const newConstraints = [...constraints];
    // Allow explicitly setting to 0 or empty string (which will be treated as 0)
    newConstraints[constraintIdx].coefficients[varIdx] = value === '' ? 0 : parseFloat(value) || 0;
    setConstraints(newConstraints);
  };
  
  // Handle constraint operator change
  const handleOperatorChange = (constraintIdx, operator) => {
    const newConstraints = [...constraints];
    newConstraints[constraintIdx].operator = operator;
    setConstraints(newConstraints);
  };
  
  // Handle RHS change
  const handleRhsChange = (constraintIdx, value) => {
    const newConstraints = [...constraints];
    newConstraints[constraintIdx].rhs = value === '' ? 0 : parseFloat(value) || 0;
    setConstraints(newConstraints);
  };
  
  // Handle objective function coefficient change
  const handleObjectiveChange = (varIdx, value) => {
    const newObjectives = [...objectiveFunctions];
    newObjectives[0].coefficients[varIdx] = value === '' ? 0 : parseFloat(value) || 0;
    setObjectiveFunctions(newObjectives);
  };
  
  // Handle goal constraint coefficient change
  const handleGoalConstraintChange = (goalIdx, varIdx, value) => {
    const newGoalConstraints = [...goalConstraints];
    newGoalConstraints[goalIdx].coefficients[varIdx] = value === '' ? 0 : parseFloat(value) || 0;
    setGoalConstraints(newGoalConstraints);
  };
  
  // Handle goal constraint operator change
  const handleGoalOperatorChange = (goalIdx, operator) => {
    const newGoalConstraints = [...goalConstraints];
    newGoalConstraints[goalIdx].operator = operator;
    setGoalConstraints(newGoalConstraints);
  };
  
  // Handle goal constraint RHS change
  const handleGoalRhsChange = (goalIdx, value) => {
    const newGoalConstraints = [...goalConstraints];
    newGoalConstraints[goalIdx].rhs = value === '' ? 0 : parseFloat(value) || 0;
    setGoalConstraints(newGoalConstraints);
  };
  
  // Handle priority change for goal programming
  const handlePriorityChange = (goalIdx, value) => {
    const newGoalConstraints = [...goalConstraints];
    newGoalConstraints[goalIdx].priority = value === '' ? 1 : parseInt(value) || 1;
    setGoalConstraints(newGoalConstraints);
  };
  
  // Solve the linear programming problem
  const solveLP = () => {
    // Reset states
    setIsLoading(true);
    setError(null);
    setSolutionData(null);
    
    // Construct the JSON payload for the backend
    const payload = {
      method: method,
      numVariables: numVariables,
      numConstraints: numConstraints,
      allNonNegative: allNonNegative,
      constraints: constraints.map(constraint => ({
        coefficients: [...constraint.coefficients],
        operator: constraint.operator,
        rhs: constraint.rhs
      }))
    };
    
    if (method === 'goalProgramming') {
      // Add goal programming specific data
      payload.numGoals = numGoals;
      payload.goals = goalConstraints.map(goal => ({
        coefficients: [...goal.coefficients],
        operator: goal.operator,
        rhs: goal.rhs,
        priority: goal.priority
      }));
    } else {
      // Add standard objective function data
      payload.optimization = isMaximize ? 'maximize' : 'minimize';
      payload.objective = {
        coefficients: [...objectiveFunctions[0].coefficients]
      };
    }
    
    fetch('http://127.0.0.1:5000/solve', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Solution data:', data);
        setSolutionData(data);
        setStep('result');
      })
      .catch((error) => {
        console.error('Error:', error);
        setError(error.message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };
  
  // Render problem setup form
  const renderSetup = () => (
    <div className="lp-solver-card">
      <h2>Setup Linear Programming Problem</h2>
      
      <div className="form-group">
        <label>Method:</label>
        <select 
          className="form-control"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
        >
          <option value="simplex">Simplex</option>
          <option value="bigM">Big M</option>
          <option value="twoPhase">Two Phase</option>
          <option value="goalProgramming">Goal Programming</option>
        </select>
      </div>
      
      <div className="form-group">
        <label>Number of Variables:</label>
        <input 
          type="number" 
          min="1"
          className="form-control"
          value={numVariables}
          onChange={(e) => setNumVariables(parseInt(e.target.value) || 1)}
        />
      </div>
      
      <div className="form-group">
        <label>Number of Constraints:</label>
        <input 
          type="number" 
          min="1"
          className="form-control"
          value={numConstraints}
          onChange={(e) => setNumConstraints(parseInt(e.target.value) || 1)}
        />
      </div>
      
      {method === 'goalProgramming' && (
        <div className="form-group">
          <label>Number of Goals:</label>
          <input 
            type="number" 
            min="1"
            className="form-control"
            value={numGoals}
            onChange={(e) => setNumGoals(parseInt(e.target.value) || 1)}
          />
        </div>
      )}
      
      {method !== 'goalProgramming' && (
        <div className="form-group">
          <label>Optimization:</label>
          <div className="radio-group">
            <label className="radio-label">
              <input 
                type="radio" 
                checked={isMaximize} 
                onChange={() => setIsMaximize(true)}
              />
              Maximize
            </label>
            <label className="radio-label">
              <input 
                type="radio" 
                checked={!isMaximize} 
                onChange={() => setIsMaximize(false)}
              />
              Minimize
            </label>
          </div>
        </div>
      )}
      
      <div className="form-group">
        <div className="checkbox-container">
          <label className="checkbox-label">
            <input 
              type="checkbox" 
              checked={allNonNegative} 
              onChange={() => setAllNonNegative(!allNonNegative)}
            />
            All variables non-negative
          </label>
        </div>
      </div>
      
      <div className="btn-container">
        <button 
          onClick={initializeMatrices}
          className="btn btn-primary"
        >
          Continue
        </button>
      </div>
    </div>
  );
  
  // Render standard objective function
  const renderStandardObjective = () => (
    <div className="section-card">
      <h3>
        {isMaximize ? "Maximize" : "Minimize"} Objective Function
      </h3>
      
      <div className="coefficient-group">
        {objectiveFunctions[0].coefficients.map((coef, varIdx) => (
          <div key={`obj-var-${varIdx}`} className="coefficient-item">
            {varIdx > 0 && <span style={{margin: '0 0.25rem'}}>+</span>}
            <input 
              type="number" 
              className="coefficient-input"
              value={coef !== 0 ? coef : ''}
              placeholder="0"
              onChange={(e) => handleObjectiveChange(varIdx, e.target.value)}
            />
            <span style={{marginLeft: '0.25rem'}}>x<sub>{varIdx+1}</sub></span>
          </div>
        ))}
      </div>
    </div>
  );
  
  // Render goal programming objectives
  const renderGoalObjectives = () => (
    <div className="section-card">
      <h3>Goal Constraints</h3>
      
      {goalConstraints.map((goal, goalIdx) => (
        <div key={`goal-${goalIdx}`} style={{marginBottom: '1.5rem'}}>
          <div style={{display: 'flex', alignItems: 'center', marginBottom: '0.5rem'}}>
            <span style={{marginRight: '0.5rem', fontWeight: '500'}}>Priority:</span>
            <input 
              type="number" 
              min="1"
              className="coefficient-input"
              value={goal.priority}
              onChange={(e) => handlePriorityChange(goalIdx, e.target.value)}
            />
          </div>
          
          <div className="coefficient-group">
            {goal.coefficients.map((coef, varIdx) => (
              <div key={`goal-${goalIdx}-var-${varIdx}`} className="coefficient-item">
                {varIdx > 0 && <span style={{margin: '0 0.25rem'}}>+</span>}
                <input 
                  type="number" 
                  className="coefficient-input"
                  value={coef !== 0 ? coef : ''}
                  placeholder="0"
                  onChange={(e) => handleGoalConstraintChange(goalIdx, varIdx, e.target.value)}
                />
                <span style={{marginLeft: '0.25rem'}}>x<sub>{varIdx+1}</sub></span>
              </div>
            ))}
            
            <select 
              className="operator-select"
              value={goal.operator}
              onChange={(e) => handleGoalOperatorChange(goalIdx, e.target.value)}
            >
              <option value="=">═</option>
              <option value="<=">≤</option>
              <option value=">=">≥</option>
            </select>
            
            <input 
              type="number" 
              className="coefficient-input"
              value={goal.rhs !== 0 ? goal.rhs : ''}
              placeholder="0"
              onChange={(e) => handleGoalRhsChange(goalIdx, e.target.value)}
            />
          </div>
        </div>
      ))}
    </div>
  );
  
  // Render input matrices
  const renderInputMatrices = () => (
    <div className="lp-solver-card">
      <h2>Input Linear Programming Problem</h2>
      
      {/* Objective Function(s) */}
      {method === 'goalProgramming' ? renderGoalObjectives() : renderStandardObjective()}
      
      {/* Constraints */}
      <div className="section-card">
        <h3>Constraints</h3>
        
        {constraints.map((constraint, constraintIdx) => (
          <div key={`constraint-${constraintIdx}`} className="coefficient-group" style={{marginBottom: '1rem'}}>
            {constraint.coefficients.map((coef, varIdx) => (
              <div key={`constraint-${constraintIdx}-var-${varIdx}`} className="coefficient-item">
                {varIdx > 0 && <span style={{margin: '0 0.25rem'}}>+</span>}
                <input 
                  type="number" 
                  className="coefficient-input"
                  value={coef !== 0 ? coef : ''}
                  placeholder="0"
                  onChange={(e) => handleConstraintChange(constraintIdx, varIdx, e.target.value)}
                />
                <span style={{marginLeft: '0.25rem'}}>x<sub>{varIdx+1}</sub></span>
              </div>
            ))}
            
            <select 
              className="operator-select"
              value={constraint.operator}
              onChange={(e) => handleOperatorChange(constraintIdx, e.target.value)}
              disabled={method === 'simplex'} // Standard simplex only allows <=
            >
              <option value="<=">≤</option>
              {method !== 'simplex' && (
                <>
                  <option value="=">═</option>
                  <option value=">=">≥</option>
                </>
              )}
            </select>
            
            <input 
              type="number" 
              className="coefficient-input"
              value={constraint.rhs !== 0 ? constraint.rhs : ''}
              placeholder="0"
              onChange={(e) => handleRhsChange(constraintIdx, e.target.value)}
            />
          </div>
        ))}
      </div>
      
      <div className="btn-container">
        <button 
          onClick={() => setStep('setup')}
          className="btn btn-secondary"
        >
          Back
        </button>
        <button 
          onClick={solveLP}
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? 'Solving...' : 'Solve'}
        </button>
      </div>
    </div>
  );
  
  // Render the current step with updated result handling
  const renderCurrentStep = () => {
    switch(step) {
      case 'setup':
        return renderSetup();
      case 'input':
        return renderInputMatrices();
      case 'result':
        if (isLoading) {
          return (
            <div className="lp-solver-card">
              <h2>Solving Problem</h2>
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>Computing solution...</p>
              </div>
            </div>
          );
        }
        
        if (error) {
          return (
            <div className="lp-solver-card">
              <h2>Error</h2>
              <div className="error-message">
                <p>An error occurred while solving the problem:</p>
                <p>{error}</p>
              </div>
              <div className="btn-container">
                <button 
                  onClick={() => setStep('input')}
                  className="btn btn-secondary"
                >
                  Back to Input
                </button>
              </div>
            </div>
          );
        }
        
        if (solutionData) {
          return renderResults(solutionData, () => setStep('input'));
        }
        
        return null;
      default:
        return renderSetup();
    }
  };
  
  return (
    <div className="lp-solver-container">
      <div className="lp-solver-wrapper">
        <h1 className="lp-solver-title">Linear Programming Solver</h1>
        {renderCurrentStep()}
      </div>
    </div>
  );
};

export default LinearProgrammingSolver;