<script>
export default {
  mounted() {
    this.getData()
  },
  data() {
    return {
      data: [],
      columns: ['Registro ANS', 'CNPJ', 'Razão Social ', 'Nome Fantasia',
        'Modalidade', 'Logradouro', 'Número', 'Complemento',
        'Bairro', 'Cidade', 'UF', 'CEP', 'DDD',
        'Telefone', 'Fax', 'Endereço eletrônico', 'Representante', 'Cargo Representante', 'Data Registro ANS'
      ],
      page: 1,
      perPage: 10,
      loading: false,
      order: true,
      order_icon: false,
      searchValue: ''
    }
  },
  computed: {
    displayedData() {
      const startIndex = Number(this.perPage) * (Number(this.page - 1));
      const endIndex = startIndex + Number(this.perPage);

      return this.data.slice(startIndex, endIndex);
    }
  },
  methods: {
    sortData(c) {
      this.order_icon = Number(c)

      const column_index = Number(c)
      this.data.sort((a, b) => {
        const x = a[column_index]
        const y = b[column_index]
        return (this.order ? x.localeCompare(y) : y.localeCompare(x));
      });


      this.order = !this.order
    },
    async getData() {
      this.page = 1
      this.loading = !this.loading

      const url = 'http://localhost:3000'
      const url_query = this.searchValue ? `?busca=${this.searchValue}` : ''

      const req = await fetch(`${url}/cadastros${url_query}`)
      const res = await req.json()

      this.data = res

      this.loading = !this.loading
    }
  }
}
</script>

<template>
  <header>
    <a href="/"><h1>Cadastros de Operadoras</h1></a>
  </header>
  <main>

    <div id="main_container">
      <div id="inputs_container">
        <div id="quantity">
          <label>Resultados por página: </label>
          <select v-model="perPage" name="btn_qtnd" id="select_p">
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </div>
        <div id="search">
          <input v-model="this.searchValue" type="text" name="busca">
          <button @click="getData">buscar</button>
        </div>
      </div>
      <h3 v-if="loading">Carregando...</h3>
      <template v-else-if="this.data.length">
        <div id="table_container">
          <table id="table_data">
            <thead>
              <tr>
                <th v-for="column in columns" :key="column" :value="columns.indexOf(column)" 
                @click="$event = sortData($event.target.attributes['value'].value)">
                  <span id="column_txt" :value="columns.indexOf(column)">
                    {{column}}
                  </span>
                  <span v-show="!order && columns.indexOf(column) == order_icon" :value="columns.indexOf(column)">
                    &#x2193;
                  </span>
                  <span v-show="order && columns.indexOf(column) == order_icon" :value="columns.indexOf(column)">
                    &#x2191;
                  </span>                  
                </th>
              </tr>
            </thead>
            <tr v-for="data in displayedData" :key="data">
              <td v-for="cadastros in data" :key="cadastros">{{ cadastros }}</td>
            </tr>
          </table>
        </div>
        <div id="pages">
          <pagination v-model="page" :records="this.data.length" :per-page="Number(perPage)"
            :options="{ texts: { count: 'Mostrando {from} até {to} de {count} resultados|{count} resultados|Um resultado' } }" />
        </div>
      </template>
      <h3 v-else>Sem resultados</h3>
    </div>

  </main>
</template>

<style scoped>
header {
  width: 100%;
  color: #fff;
  background: #324960;
  padding: 1em;
  font-size: max(20px, 1em);
}

#main_container {
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#inputs_container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin: 0 auto;
  padding: 1em;
  width: 80%;
  height: 100px;
  color: #ffffff;
}

#quantity,
#search {
  margin: 0 auto;
}

#quantity select {
  color: #fff;
  background: none;
  border: none;
  border-bottom: 1px solid #324960;
}

#select_p {
  cursor: pointer;
}

#select_p option {
  background: #181818
}

#search input {
  background-color: transparent;
  margin-right: 10px;
  border: none;
  color: #fff;
  border-bottom: 1px solid #324960;
}

#search button {
  cursor: pointer;
  padding: 7px;
  background: none;
  color: #ffffff;
  border: 1px solid #324960;
  border-radius: 10px;
}

#search button:active {
  background: #617a92;
}

#table_container {
  color: rgb(0, 0, 0);
  background-color: #f8f8f8;
  margin: 0 auto;
  width: 90%;
  height: min(600px, 50em);
  overflow: auto;
}

#table_data {
  table-layout: fixed;
  margin: 0 auto;
  font-size: 14px;
  border-collapse: collapse;
  white-space: break-spaces;
  word-wrap: break-word;
  background-color: #fff;
  width: 100%;
}

#table_data td, th {
  width: 150px;
  height: 70px;
  text-align: center;
  padding: 5px;
}

#table_data td {
  border-right: 1px solid #f8f8f8;
  font-size: 12px;
}

#table_data thead th {
  cursor: pointer;
  color: #ffffff;
  background: #4FC3A1;
}

#table_data thead th:nth-child(odd) {
  color: #ffffff;
  background: #324960;
}

#table_data tr:nth-child(even) {
  background: #F4F4F4;
}

#pages {
  /* background-color: pink; */
  overflow: auto;
  color: #ffffff;
  text-align: center;
}

@media (max-width: 767px) {
  #table_data fl-table {
    display: block;
    width: 100%;
  }

  #table_data fl-table thead,
  #table_data fl-table tbody,
  #table_data fl-table thead th {
    display: block;
  }

  #table_data fl-table thead th:last-child {
    border-bottom: none;
  }

  #table_data fl-table thead {
    float: left;
  }

  #table_data fl-table tbody {
    width: auto;
    position: relative;
    overflow-x: auto;
  }

  #table_data fl-table td,
  #table_data fl-table th {
    padding: 20px .625em .625em .625em;
    height: 60px;
    vertical-align: middle;
    box-sizing: border-box;
    overflow-x: hidden;
    overflow-y: auto;
    width: 120px;
    font-size: 13px;
    text-overflow: ellipsis;
  }

  #table_data fl-table thead th {
    text-align: left;
    border-bottom: 1px solid #f7f7f9;
  }

  #table_data fl-table tbody tr {
    display: table-cell;
  }

  #table_data fl-table tbody tr:nth-child(odd) {
    background: none;
  }

  #table_data fl-table tr:nth-child(even) {
    background: transparent;
  }

  #table_data fl-table tr td:nth-child(odd) {
    background: #F8F8F8;
    border-right: 1px solid #E6E4E4;
  }

  #table_data fl-table tr td:nth-child(even) {
    border-right: 1px solid #E6E4E4;
  }

  #table_data fl-table tbody td {
    display: block;
    text-align: center;
  }
}
</style>
