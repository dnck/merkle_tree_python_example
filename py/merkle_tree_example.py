import random
import hashlib
# Code modified from:
# https://www.codementor.io/blog/merkle-trees-5h9arzd3n8
# Other helpful resources:
# https://prathamudeshmukh.github.io/merkle-tree-demo/

# Break a string up into roughly equal chunks
def get_chunks(s, chunks_size):
    chunks = []
    for i in range(0, len(s), chunks_size):
        chunks.append( s[i:i+chunks_size] )
    return chunks

class MerkleNode:
    """
    Stores the hash and the parent.
    """
    def __init__(self, _hash):
        self._hash = _hash
        self.parent = None
        self.left_child = None
        self.right_child = None

class MerkleTree:
    """
    Stores the leaves and the root hash of the tree.
    """
    def __init__(self, data_chunks):

        self.leaves = []

        for chunk in data_chunks:

            node = MerkleNode(self.compute_hash(chunk))

            self.leaves.append(node)

        self.root = self.build_merkle_tree(self.leaves)

    def build_merkle_tree(self, leaves):
        """
        Builds the Merkle tree from a list of leaves.
        In case of an odd number of leaves, the last leaf is duplicated.
        """
        num_leaves = len(leaves)

        if num_leaves == 1:

            return leaves[0]

        parents = []

        i = 0
        while i < num_leaves:

            left_child = leaves[i]

            if i + 1 < num_leaves:

                right_child = leaves[i + 1]

            else:

                right_child = left_child

            parents.append(self.create_parent(left_child, right_child))

            i += 2

        return self.build_merkle_tree(parents)

    def create_parent(self, left_child, right_child):

        parent = MerkleNode(self.compute_hash(left_child._hash + right_child._hash))

        parent.left_child, parent.right_child = left_child, right_child

        left_child.parent, right_child.parent = parent, parent

        return parent

    @staticmethod
    def compute_hash(data):

        data = data.encode('utf-8')

        return hashlib.sha256(data).hexdigest()

    def get_audit_trail(self, chunk_hash):
        """
        Checks if the leaf exists, and returns the audit trail
        in case it does.
        """
        for leaf in self.leaves:

            if leaf._hash == chunk_hash:

                print("Leaf exists")
                #print(leaf._hash , chunk_hash )

                return self.generate_audit_trail(leaf, trail=[])

        return False

    def generate_audit_trail(self, merkle_node, trail=[]):
        """
        Generates the audit trail in a bottom-up fashion
        """
        #print(merkle_node._hash)
        if merkle_node == self.root:

            trail.append(merkle_node._hash)

            return trail

        # check if the merkle_node is the left child or the right child
        is_left = merkle_node.parent.left_child == merkle_node

        if is_left:

            # since the current node is left child, right child is
            # needed for the audit trail. We'll need this info later
            # for audit proof.
            trail.append((merkle_node.parent.right_child._hash, False))

            return self.generate_audit_trail(merkle_node.parent, trail)

        else:

            trail.append((merkle_node.parent.left_child._hash, True))

            return self.generate_audit_trail(merkle_node.parent, trail)

class Validator:

    def __init__(self):

        pass

    def verify_audit_trail(chunk_hash, audit_trail):
        """
        Performs the audit-proof from the audit_trail received
        from the trusted server.
        """
        proof_till_now = chunk_hash

        for node in audit_trail[:-1]:

            _hash = node[0]

            is_left = node[1]

            if is_left:

                # the order of hash concatenation depends on whether the
                # the node is a left child or right child of its parent

                proof_till_now = MerkleTree.compute_hash(_hash + proof_till_now)

            else:

                proof_till_now = MerkleTree.compute_hash(proof_till_now + _hash)

            print(proof_till_now)

        # verifying the computed root hash against the actual root hash
        return proof_till_now == audit_trail[-1]

if __name__ == "__main__":
    dna_bases = {1:"A", 2:"G", 3:"C", 4:"T"}
    get_genomic_sequence = lambda dna_bases, N : ''.join([dna_bases[random.choice(range(1, 5))] for i in range(N)])
    dna_strand = get_genomic_sequence(dna_bases, 1000)
    print("File sequence: {}".format(dna_strand))
    print("")
    print("Chunking sequence...")
    chunks = get_chunks(dna_strand, 20)
    print("")
    print("Scattering chunks and storing merkle root of chunks on server...")
    print("")
    merkle_tree = MerkleTree(chunks)
    chunk_hash = MerkleTree.compute_hash(chunks[33])
    print("Server stored the merkle root of the chunks as {}".format(merkle_tree.root._hash))
    print("")
    print("Unknown client downloading chunk {} from a p2p network.".format(chunk_hash))
    print("")
    print("Client requesting audit trail for downloaded chunk from server...")
    print("")
    print("Server response ... ")
    audit_trail = merkle_tree.get_audit_trail(chunk_hash)
    print("")
    print("Server response with audit trail for chunk: {}".format(audit_trail))
    print("")
    print("Client check on chunk status ... ")
    Validator.verify_audit_trail(chunk_hash, audit_trail)
