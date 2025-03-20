import React, { useState } from 'react';
import './linearSolver.css';

const LinearProgrammingSolver = () => {
  // State for method selection
  const [method, setMethod] = useState('simplex');
  
  // State for problem dimensions
  const [numVariables, setNumVariables] = useState(2);
  const [numConstraints, setNumConstraints] = useState(2);
  const [numGoals, setNumGoals] = useState(1);
  
  // State for setup step
  const [step, setStep] = useState('setup'); // 'setup', 'input', 'result'
  
  // State for constraints and objective function
  const [constraints, setConstraints] = useState([]);
  const [objectiveFunctions, setObjectiveFunctions] = useState([]);
  const [isMaximize, setIsMaximize] = useState(true);
  
  // Initialize matrices when dimensions are set
  const initializeMatrices = () => {
    // Initialize constraints matrix
    const newConstraints = Array(numConstraints).fill().map(() => ({
      coefficients: Array(numVariables).fill(0),
      operator: '<=',
      rhs: 0
    }));
    setConstraints(newConstraints);
    
    // Initialize objective function(s)
    const objFunctions = method === 'goalProgramming' 
      ? Array(numGoals).fill().map(() => ({
          coefficients: Array(numVariables).fill(0),
          priority: 1
        }))
      : [{
          coefficients: Array(numVariables).fill(0)
        }];
    setObjectiveFunctions(objFunctions);
    
    setStep('input');
  };
  
  // Handle constraint coefficient change
  const handleConstraintChange = (constraintIdx, varIdx, value) => {
    const newConstraints = [...constraints];
    newConstraints[constraintIdx].coefficients[varIdx] = parseFloat(value) || 0;
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
    newConstraints[constraintIdx].rhs = parseFloat(value) || 0;
    setConstraints(newConstraints);
  };
  
  // Handle objective function coefficient change
  const handleObjectiveChange = (objIdx, varIdx, value) => {
    const newObjectives = [...objectiveFunctions];
    newObjectives[objIdx].coefficients[varIdx] = parseFloat(value) || 0;
    setObjectiveFunctions(newObjectives);
  };
  
  // Handle priority change for goal programming
  const handlePriorityChange = (objIdx, value) => {
    const newObjectives = [...objectiveFunctions];
    newObjectives[objIdx].priority = parseInt(value) || 1;
    setObjectiveFunctions(newObjectives);
  };
  
  // Solve the LP problem (placeholder)
  const solveLP = () => {
    // Here you would implement or call your LP solver
    console.log("Solving LP with method:", method);
    console.log("Constraints:", constraints);
    console.log("Objective Functions:", objectiveFunctions);
    console.log("Maximize:", isMaximize);
    
    // For now, just switch to result view
    setStep('result');
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
  
  // Render input matrices
  const renderInputMatrices = () => (
    <div className="lp-solver-card">
      <h2>Input Linear Programming Problem</h2>
      
      {/* Objective Function(s) */}
      <div className="section-card">
        <h3>
          {isMaximize ? "Maximize" : "Minimize"} {method === 'goalProgramming' ? "Goals" : "Objective Function"}
        </h3>
        
        {objectiveFunctions.map((objFunc, objIdx) => (
          <div key={`obj-${objIdx}`} style={{marginBottom: '1rem'}}>
            {method === 'goalProgramming' && (
              <div style={{display: 'flex', alignItems: 'center', marginBottom: '0.5rem'}}>
                <span style={{marginRight: '0.5rem', fontWeight: '500'}}>Priority:</span>
                <input 
                  type="number" 
                  min="1"
                  className="coefficient-input"
                  value={objFunc.priority}
                  onChange={(e) => handlePriorityChange(objIdx, e.target.value)}
                />
              </div>
            )}
            
            <div className="coefficient-group">
              {objFunc.coefficients.map((coef, varIdx) => (
                <div key={`obj-${objIdx}-var-${varIdx}`} className="coefficient-item">
                  {varIdx > 0 && <span style={{margin: '0 0.25rem'}}>+</span>}
                  <input 
                    type="number" 
                    className="coefficient-input"
                    value={coef !== 0 ? coef : ''}
                    onChange={(e) => handleObjectiveChange(objIdx, varIdx, e.target.value)}
                  />
                  <span style={{marginLeft: '0.25rem'}}>x<sub>{varIdx+1}</sub></span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      
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
              value={constraint.rhs}
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
        >
          Solve
        </button>
      </div>
    </div>
  );
  
  // Render results (placeholder)
  const renderResults = () => (
    <div className="lp-solver-card">
      <h2>Results</h2>
      <p className="text-center" style={{marginBottom: '1rem'}}>This is where the solution would be displayed.</p>
      <p className="text-center text-gray" style={{marginBottom: '1rem'}}>
        For a complete implementation, you would need to connect this UI to a backend solver or implement the solver in JavaScript.
      </p>
      
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
  
  // Render the current step
  const renderCurrentStep = () => {
    switch(step) {
      case 'setup':
        return renderSetup();
      case 'input':
        return renderInputMatrices();
      case 'result':
        return renderResults();
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