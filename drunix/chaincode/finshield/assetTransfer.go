/*
SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"log"

	"github.com/hyperledger/fabric-contract-api-go/v2/contractapi"
	"github.com/Sarah-pix/FinShield-360/drunix/chaincode/finshield/chaincode"
)

func main() {

	finshieldChaincode, err := contractapi.NewChaincode(
		&chaincode.SmartContract{},
	)

	if err != nil {
		log.Panicf("Error creating FinShield chaincode: %v", err)
	}

	if err := finshieldChaincode.Start(); err != nil {
		log.Panicf("Error starting FinShield chaincode: %v", err)
	}
}
