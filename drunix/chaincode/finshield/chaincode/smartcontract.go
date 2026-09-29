package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/v2/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

// Payment represents a FinShield financial transaction.
type Payment struct {
	Amount     float64 `json:"amount"`
	Currency   string  `json:"currency"`
	Decision   string  `json:"decision"`
	PaymentID  string  `json:"paymentId"`
	Receiver   string  `json:"receiver"`
	RiskLevel  string  `json:"riskLevel"`
	RiskScore  int     `json:"riskScore"`
	Sender     string  `json:"sender"`
	Status     string  `json:"status"`
}

// CreatePayment creates a new payment record.
func (s *SmartContract) CreatePayment(
	ctx contractapi.TransactionContextInterface,
	paymentID string,
	sender string,
	receiver string,
	amount float64,
	currency string,
	riskScore int,
	riskLevel string,
	decision string,
	status string,
) error {

	exists, err := s.PaymentExists(ctx, paymentID)
	if err != nil {
		return err
	}

	if exists {
		return fmt.Errorf("payment %s already exists", paymentID)
	}

	payment := Payment{
		PaymentID: paymentID,
		Sender:    sender,
		Receiver:  receiver,
		Amount:    amount,
		Currency:  currency,
		RiskScore: riskScore,
		RiskLevel: riskLevel,
		Decision:  decision,
		Status:    status,
	}

	paymentJSON, err := json.Marshal(payment)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(paymentID, paymentJSON)
}

// ReadPayment retrieves a payment.
func (s *SmartContract) ReadPayment(
	ctx contractapi.TransactionContextInterface,
	paymentID string,
) (*Payment, error) {

	paymentJSON, err := ctx.GetStub().GetState(paymentID)

	if err != nil {
		return nil, fmt.Errorf("failed to read payment: %v", err)
	}

	if paymentJSON == nil {
		return nil, fmt.Errorf("payment %s does not exist", paymentID)
	}

	var payment Payment

	err = json.Unmarshal(paymentJSON, &payment)
	if err != nil {
		return nil, err
	}

	return &payment, nil
}

// UpdatePayment updates an existing payment.
func (s *SmartContract) UpdatePayment(
	ctx contractapi.TransactionContextInterface,
	paymentID string,
	riskScore int,
	riskLevel string,
	decision string,
	status string,
) error {

	payment, err := s.ReadPayment(ctx, paymentID)

	if err != nil {
		return err
	}

	payment.RiskScore = riskScore
	payment.RiskLevel = riskLevel
	payment.Decision = decision
	payment.Status = status

	paymentJSON, err := json.Marshal(payment)

	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(paymentID, paymentJSON)
}

// PaymentExists checks whether a payment exists.
func (s *SmartContract) PaymentExists(
	ctx contractapi.TransactionContextInterface,
	paymentID string,
) (bool, error) {

	paymentJSON, err := ctx.GetStub().GetState(paymentID)

	if err != nil {
		return false, fmt.Errorf("failed to check payment: %v", err)
	}

	return paymentJSON != nil, nil
}

// GetAllPayments returns all FinShield payments.
func (s *SmartContract) GetAllPayments(
	ctx contractapi.TransactionContextInterface,
) ([]*Payment, error) {

	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")

	if err != nil {
		return nil, err
	}

	defer resultsIterator.Close()

	var payments []*Payment

	for resultsIterator.HasNext() {

		queryResponse, err := resultsIterator.Next()

		if err != nil {
			return nil, err
		}

		var payment Payment

		err = json.Unmarshal(queryResponse.Value, &payment)

		if err != nil {
			return nil, err
		}

		payments = append(payments, &payment)
	}

	return payments, nil
}
