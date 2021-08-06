#!/usr/bin/env python3

import connexion
from swagger_server import encoder
from modelling import clustering
from modelling import decision_tree
from utilities import glb_handles
from flask_cors import CORS, cross_origin



def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'AIRservices'}, pythonic_params=True)

    # build models before running the server
    glb_handles.canc_root_node, glb_handles.canc_dt, glb_handles.delay_root_node, glb_handles.delay_dt = decision_tree.create_decision_tree() 
    glb_handles.cluster_model, glb_handles.cluster_df = clustering.cluster()    

    CORS(app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
