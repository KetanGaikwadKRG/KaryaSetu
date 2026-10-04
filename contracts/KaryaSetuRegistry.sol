// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title KaryaSetuRegistry
 * @dev Cryptographic Provenance & Tamper-Verification Registry for KaryaSetu AI (SIH 2026).
 *
 * Implements strict access control (onlyRelayer) to prevent malicious pre-registration
 * or front-running of document artifact hashes.
 */
contract KaryaSetuRegistry {
    address public owner;
    mapping(address => bool) public authorizedRelayers;

    struct IntegrityRecord {
        bool exists;
        uint256 timestamp;
        bytes32 provenanceHash;
        address recorder;
    }

    // artifactHash => IntegrityRecord
    mapping(bytes32 => IntegrityRecord) private registry;

    event DigestAnchored(
        bytes32 indexed artifactHash,
        bytes32 indexed provenanceHash,
        address indexed recorder,
        uint256 timestamp
    );

    event RelayerStatusUpdated(address indexed relayer, bool status);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "KaryaSetuRegistry: caller is not the owner");
        _;
    }

    modifier onlyRelayer() {
        require(
            msg.sender == owner || authorizedRelayers[msg.sender],
            "KaryaSetuRegistry: caller is not an authorized relayer"
        );
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedRelayers[msg.sender] = true;
        emit RelayerStatusUpdated(msg.sender, true);
    }

    function setRelayer(address relayer, bool status) external onlyOwner {
        require(relayer != address(0), "Invalid relayer address");
        authorizedRelayers[relayer] = status;
        emit RelayerStatusUpdated(relayer, status);
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid new owner");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    /**
     * @notice Records an artifact hash and associated provenance hash on-chain.
     * @dev Restricted to authorized relayer addresses to prevent hash spoofing.
     */
    function recordDigest(bytes32 artifactHash, bytes32 provenanceHash) external onlyRelayer {
        require(artifactHash != bytes32(0), "Invalid artifact hash");
        require(!registry[artifactHash].exists, "Artifact hash already registered");

        registry[artifactHash] = IntegrityRecord({
            exists: true,
            timestamp: block.timestamp,
            provenanceHash: provenanceHash,
            recorder: msg.sender
        });

        emit DigestAnchored(artifactHash, provenanceHash, msg.sender, block.timestamp);
    }

    /**
     * @notice Verifies whether a given artifact hash is recorded in the registry.
     * @param artifactHash SHA-256 hash of the deliverable artifact.
     * @return exists True if the digest is registered.
     * @return timestamp Block timestamp when the digest was anchored.
     * @return provenanceHash Hash representing the upstream source & pipeline context.
     * @return recorder Address that submitted the anchoring transaction.
     */
    function verifyDigest(bytes32 artifactHash)
        external
        view
        returns (
            bool exists,
            uint256 timestamp,
            bytes32 provenanceHash,
            address recorder
        )
    {
        IntegrityRecord memory rec = registry[artifactHash];
        return (rec.exists, rec.timestamp, rec.provenanceHash, rec.recorder);
    }
}
